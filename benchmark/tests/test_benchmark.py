"""Pruebas del oráculo, del parser y del análisis de resultados.

    .venv/Scripts/python.exe -m unittest discover -s benchmark/tests -v
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import deadline_math as dm  # noqa: E402
import kaggle_resultados as kr  # noqa: E402


class Oraculo(unittest.TestCase):
    def test_respuesta_a_mano_igual_a_la_calculada_en_los_31_casos(self):
        self.assertEqual(len(dm.CASES), 20)
        self.assertEqual(len(dm.CASES_HARD), 11)
        for case in dm.ALL_CASES:
            with self.subTest(case=case.id):
                self.assertEqual(dm.computed_answer(case), case.expected)

    def test_ids_unicos(self):
        ids = [c.id for c in dm.ALL_CASES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_cierre_de_este_reto(self):
        roll_1 = next(c for c in dm.CASES if c.id == "roll-1")
        self.assertEqual(roll_1.expected, "2026-10-12 08:59")

    def test_duracion_en_tiempo_absoluto_y_no_de_reloj(self):
        # La trampa que cayó en el propio oráculo: con ZoneInfo, aware + timedelta suma horas de reloj.
        inicio = datetime(2026, 10, 24, 18, 0, tzinfo=ZoneInfo("Europe/Madrid"))
        self.assertEqual((inicio + timedelta(hours=48)).strftime("%H:%M"), "18:00")  # la trampa
        h_dur_1 = next(c for c in dm.CASES_HARD if c.id == "h-dur-1")
        self.assertEqual(dm.computed_answer(h_dur_1), "2026-10-26 17:00")  # lo correcto

    def test_semana_de_dst_desfasado(self):
        dst_oct_1 = next(c for c in dm.CASES if c.id == "dst-oct-1")
        self.assertEqual(dm.computed_answer(dst_oct_1), "2026-10-29 07:59")  # 8 h, no las 9 de siempre


def _domingo(anyo: int, mes: int, n: int) -> datetime:
    """n-ésimo domingo del mes (n = -1: el último)."""
    if n > 0:
        dia = datetime(anyo, mes, 1)
        dia += timedelta(days=(6 - dia.weekday()) % 7)
        return dia + timedelta(weeks=n - 1)
    siguiente = datetime(anyo + (mes == 12), mes % 12 + 1, 1)
    dia = siguiente - timedelta(days=1)
    return dia - timedelta(days=(dia.weekday() - 6) % 7)


# Segundo oráculo, sin zoneinfo: zona -> (región, desfase estándar en horas).
REGLAS = {"America/Los_Angeles": ("US", -8), "America/New_York": ("US", -5), "Europe/Madrid": ("EU", 1),
          "Europe/Berlin": ("EU", 1), "Europe/London": ("EU", 0)}


def _desfase_utc(zona: str, utc: datetime) -> timedelta:
    """Desfase de la zona en un instante UTC (naive), con las reglas de 2026 escritas a mano."""
    region, estandar = REGLAS[zona]
    if region == "US":  # del 2.º domingo de marzo a las 2:00 locales al 1.er domingo de noviembre a las 2:00
        inicio = _domingo(utc.year, 3, 2) + timedelta(hours=2 - estandar)
        fin = _domingo(utc.year, 11, 1) + timedelta(hours=2 - (estandar + 1))
    else:  # UE: del último domingo de marzo al último de octubre, a la 01:00 UTC
        inicio = _domingo(utc.year, 3, -1) + timedelta(hours=1)
        fin = _domingo(utc.year, 10, -1) + timedelta(hours=1)
    return timedelta(hours=estandar + (inicio <= utc < fin))


def _a_utc(zona: str, local: datetime) -> datetime:
    candidatos = [local - timedelta(hours=h) for h in (REGLAS[zona][1], REGLAS[zona][1] + 1)]
    validos = [u for u in candidatos if local - u == _desfase_utc(zona, u)]
    assert len(validos) == 1, (zona, local)  # el diseño evita horas inexistentes o repetidas
    return validos[0]


class OraculoIndependiente(unittest.TestCase):
    def test_reglas_escritas_a_mano(self):
        self.assertEqual(_domingo(2026, 3, 2), datetime(2026, 3, 8))
        self.assertEqual(_domingo(2026, 11, 1), datetime(2026, 11, 1))
        self.assertEqual(_domingo(2026, 3, -1), datetime(2026, 3, 29))
        self.assertEqual(_domingo(2026, 10, -1), datetime(2026, 10, 25))

    def test_los_100_casos_de_pares_coinciden_con_zoneinfo(self):
        self.assertEqual(len(dm.CASES_PAIRS), 100)
        for case in dm.CASES_PAIRS:
            with self.subTest(case=case.id):
                local = datetime.strptime(case.source_local, "%Y-%m-%d %H:%M")
                utc = _a_utc(case.source_zone, local) + timedelta(minutes=case.shift_minutes)
                lector = dm.READERS[case.reader]
                respuesta = utc + _desfase_utc(lector, utc)
                self.assertEqual(respuesta.strftime("%Y-%m-%d %H:%M"), case.expected)

    def test_respuesta_ingenua(self):
        for case in dm.CASES_PAIRS:
            with self.subTest(case=case.id):
                local = datetime.strptime(case.source_local, "%Y-%m-%d %H:%M")
                if case.shift_minutes:  # duración: sumar horas de reloj
                    ingenua = local + timedelta(minutes=case.shift_minutes)
                else:  # conversión: la diferencia de julio, cuando los dos lados están en horario de verano
                    julio = datetime(2026, 7, 1, 12)
                    ingenua = local + _desfase_utc(dm.READERS[case.reader], julio) - _desfase_utc(case.source_zone, julio)
                self.assertEqual(ingenua.strftime("%Y-%m-%d %H:%M"), case.naive)
                es_trampa = case.category.endswith("-trap")
                self.assertEqual(case.naive != case.expected, es_trampa)

    def test_cada_trampa_tiene_su_control(self):
        ids = {c.id for c in dm.CASES_PAIRS}
        trampas = [c for c in dm.CASES_PAIRS if c.id.endswith("-T")]
        self.assertEqual(len(trampas), 50)
        for trampa in trampas:
            control = next(c for c in dm.CASES_PAIRS if c.id == trampa.id[:-1] + "C")
            self.assertIn(control.id, ids)
            self.assertEqual(trampa.reader, control.reader)
            self.assertEqual(trampa.source_zone, control.source_zone)
            self.assertEqual(trampa.source_local[11:], control.source_local[11:])  # misma hora de reloj
            self.assertEqual(datetime.strptime(trampa.source_local[:10], "%Y-%m-%d").weekday(),
                             datetime.strptime(control.source_local[:10], "%Y-%m-%d").weekday())


class AnalisisPares(unittest.TestCase):
    def test_estadisticos(self):
        import analisis_pares as ap
        bajo, alto = ap.wilson(5, 10)
        self.assertAlmostEqual(bajo, 0.2366, places=3)
        self.assertAlmostEqual(alto, 0.7634, places=3)
        self.assertAlmostEqual(ap.binomial_dos_colas(0, 10), 2 / 1024)
        self.assertEqual(ap.binomial_dos_colas(5, 10), 1.0)

    def test_modelo_que_aplica_siempre_la_diferencia_habitual(self):
        import analisis_pares as ap
        casos = {}
        for c in dm.CASES_PAIRS:  # acierta los controles y en las trampas da la respuesta ingenua
            casos[c.id] = ("ok", f"ANSWER: {c.expected}") if c.id.endswith("-C") else ("wrong", f"ANSWER: {c.naive}")
        casos["pc-aut-01-T"] = ("infra", None)  # este par entero queda fuera
        texto = ap.informe({"m/a": casos, "m/b": casos}, "prueba")
        self.assertIn("| m/a | 49 | 0% [0%–7%] | 100% [93%–100%] | +100% | 49 / 0 |", texto)
        self.assertIn("**H1** — penalización media de la cohorte: **+100.0%**", texto)
        self.assertIn("**98/98**", texto)
        self.assertIn("Se sostiene** (criterio: límite inferior > 50 %)", texto)


class Prompts(unittest.TestCase):
    def test_prompt_estandar_no_cambia(self):
        # Si este texto cambia, las ejecuciones ya hechas dejan de ser comparables.
        base_1 = dm.CASES[0]
        self.assertEqual(
            dm.PROMPTS["direct"].format(reader=base_1.reader, statement=base_1.statement, target=base_1.target),
            'I live in Madrid, Spain. A contest page says: "Submissions close September 30, 2026 at 5:00 PM ET."\n'
            "When is that deadline in my local time? Reply with exactly one line and nothing else: "
            "ANSWER: YYYY-MM-DD HH:MM (24-hour clock, my local time).",
        )


class Parser(unittest.TestCase):
    def test_formatos_aceptados(self):
        self.assertEqual(dm.parse_answer("ANSWER: 2026-10-12 08:59"), "2026-10-12 08:59")
        self.assertEqual(dm.parse_answer("**ANSWER:** 2026-10-12 08:59"), "2026-10-12 08:59")  # negrita de Markdown
        self.assertEqual(dm.parse_answer("ANSWER: **2026-10-12 08:59**"), "2026-10-12 08:59")
        self.assertEqual(dm.parse_answer("ANSWER: 2026-10-12T8:59"), "2026-10-12 08:59")

    def test_gana_la_ultima_linea_answer(self):
        texto = "Primero pensé ANSWER: 2026-10-12 10:59\npero no.\nANSWER: 2026-10-12 08:59"
        self.assertEqual(dm.parse_answer(texto), "2026-10-12 08:59")

    def test_sin_answer(self):
        self.assertIsNone(dm.parse_answer("The deadline is 2026-10-12 08:59."))
        self.assertIsNone(dm.parse_answer(""))


class Clasificacion(unittest.TestCase):
    def test_estados(self):
        self.assertEqual(kr.clasificar(None, "2026-10-12 08:59", None, None), "infra")
        self.assertEqual(kr.clasificar("ANSWER: 2026-10-12 08:59", "2026-10-12 08:59", None, None), "ok")
        self.assertEqual(kr.clasificar("ANSWER: 2026-10-12 10:59", "2026-10-12 08:59", None, None), "wrong")
        self.assertEqual(kr.clasificar("It is 08:59.", "2026-10-12 08:59", None, None), "no_answer")
        self.assertEqual(kr.clasificar("It is 08:5", "2026-10-12 08:59", 8192, 8000), "truncated")

    def test_formato_estricto(self):
        self.assertTrue(kr.STRICT_RE.fullmatch("ANSWER: 2026-10-12 08:59"))
        self.assertFalse(kr.STRICT_RE.fullmatch("PDT is UTC-7.\nANSWER: 2026-10-12 08:59"))
        self.assertFalse(kr.STRICT_RE.fullmatch("ANSWER: 2026-10-12 08:59 (24-hour clock, my local time)."))


def _escribir_ejecucion(raiz: Path, task: str, version: int, modelo: str, respuestas: dict[str, str | None],
                        estado: str = "BENCHMARK_TASK_RUN_STATE_COMPLETED", prompt_extra: str = "") -> None:
    """Crea una ejecución descargada mínima (run.json + atif.json) con las respuestas dadas por caso."""
    juego, modo = kr.PROTOCOLO[task].juego, kr.PROTOCOLO[task].modo
    carpeta = raiz / task / str(version) / modelo.split("/")[-1] / "1"
    carpeta.mkdir(parents=True)
    aserciones, trayectorias = [], []
    for case in dm.CASE_SETS[juego]:
        respuesta = respuestas.get(case.id, f"ANSWER: {case.expected}")
        ok = respuesta is not None and dm.parse_answer(respuesta) == case.expected
        aserciones.append({"expectation": f"[{case.category}] {case.id}: x",
                           "status": "BENCHMARK_TASK_RUN_ASSERTION_STATUS_" + ("PASSED" if ok else "FAILED")})
        prompt = dm.PROMPTS[modo].format(reader=case.reader, statement=case.statement, target=case.target)
        pasos = [{"source": "user", "message": prompt + prompt_extra}]
        if respuesta is not None:
            pasos.append({"source": "agent", "message": respuesta})
        trayectorias.append({"agent": {"name": f"{case.id}-try1"}, "steps": pasos})
    run = {"modelVersion": {"slug": modelo}, "state": estado, "assertions": aserciones, "errorMessage": ""}
    (carpeta / "x.run.json").write_text(json.dumps(run), encoding="utf-8")
    (carpeta / "x.atif.json").write_text(json.dumps({"subagent_trajectories": trayectorias}), encoding="utf-8")


class Analisis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        self.raiz_original, kr.RAIZ = kr.RAIZ, self.raiz

    def tearDown(self):
        kr.RAIZ = self.raiz_original
        self.tmp.cleanup()

    def test_version_excluida_no_cuenta(self):
        _escribir_ejecucion(self.raiz, "deadline-math-direct", 2, "m/a", {})
        resultado, _ = kr.leer("deadline-math-direct")
        self.assertNotIn("m/a", resultado)

    def test_version_nueva_entra_sola_con_su_limite(self):
        _escribir_ejecucion(self.raiz, "deadline-math-direct", 12, "m/a", {})
        ej = kr.elegida(kr.leer_task("deadline-math-direct")["m/a"])
        self.assertEqual(ej.version, 12)
        self.assertEqual(kr.PROTOCOLO["deadline-math-direct"].limite(12), 8192)
        self.assertIsNone(kr.PROTOCOLO["deadline-math-direct"].limite(3))

    def test_gana_la_ultima_ejecucion_limpia_y_se_informa_su_version(self):
        _escribir_ejecucion(self.raiz, "deadline-math-reasoned", 3, "m/a", {"base-1": "ANSWER: 2000-01-01 00:00"})
        _escribir_ejecucion(self.raiz, "deadline-math-reasoned", 7, "m/a", {})
        ej = kr.elegida(kr.leer_task("deadline-math-reasoned")["m/a"])
        self.assertEqual(ej.version, 7)
        self.assertEqual(list(ej.casos.values()).count("ok"), 20)

    def test_si_la_nueva_falla_por_infra_se_conserva_la_anterior_limpia(self):
        _escribir_ejecucion(self.raiz, "deadline-math-reasoned", 3, "m/a", {})
        _escribir_ejecucion(self.raiz, "deadline-math-reasoned", 7, "m/a", {"base-1": None})
        ej = kr.elegida(kr.leer_task("deadline-math-reasoned")["m/a"])
        self.assertEqual(ej.version, 3)

    def test_casos_sin_respuesta_son_infra_y_no_fallo(self):
        _escribir_ejecucion(self.raiz, "deadline-math-reasoned", 3, "m/a", {"base-1": None})
        resultado, fallidas = kr.leer("deadline-math-reasoned")
        self.assertNotIn("m/a", resultado)
        self.assertIn("m/a", fallidas)

    def test_prompt_distinto_se_descarta(self):
        _escribir_ejecucion(self.raiz, "deadline-math-reasoned", 3, "m/a", {}, prompt_extra=" (old)")
        ej = kr.leer_task("deadline-math-reasoned")["m/a"][0]
        self.assertFalse(ej.limpia)
        self.assertEqual(kr._causa([ej]), "prompt distinto del actual")

    def test_clasificacion_coincide_con_la_asercion(self):
        _escribir_ejecucion(self.raiz, "deadline-math-hard-direct", 1, "m/a", {"h-fmt-1": "ANSWER: 2026-10-11 15:59"})
        ej = kr.leer_task("deadline-math-hard-direct")["m/a"][0]
        self.assertEqual(ej.casos["h-fmt-1"], "wrong")
        self.assertEqual(ej.discrepancias, [])


if __name__ == "__main__":
    unittest.main()
