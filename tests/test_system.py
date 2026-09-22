import csv
import tempfile
import unittest
from pathlib import Path

from adaptation_factor import AdaptationStore, Estimate, StressBand, calculate_estress, classify_stress


class ModelTests(unittest.TestCase):
    def test_difference_in_differences(self):
        self.assertEqual(calculate_estress(850, 500, 1000, 900), 250)

    def test_stress_bands_and_invalid_baseline(self):
        self.assertEqual(classify_stress(100, 80), StressBand.MODERATE)
        with self.assertRaisesRegex(ValueError, "external counterfactual"):
            classify_stress(0, -1)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "test.db"
        self.store = AdaptationStore(self.db)
        self.store.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def estimate(self, study_id="one", unit="usd", effect=10, weight=1):
        return Estimate(study_id, "innovation", "control", "place", "income", unit,
                        "RCT", StressBand.SEVERE, effect, weight=weight)

    def test_store_and_weighted_aggregate(self):
        self.store.add(self.estimate(effect=10, weight=1))
        self.store.add(self.estimate("two", effect=20, weight=3))
        result = self.store.aggregate("usd")
        self.assertEqual(result, {"outcome_unit": "usd", "n": 2, "factor": 17.5, "total_weight": 4.0})

    def test_units_are_not_mixed(self):
        self.store.add(self.estimate())
        self.store.add(self.estimate("two", "kg", 99))
        self.assertEqual(self.store.aggregate("usd")["factor"], 10)

    def test_csv_four_cell_calculation(self):
        path = Path(self.temp.name) / "data.csv"
        fields = ["study_id","innovation","comparator","context","outcome","outcome_unit","method",
                  "stress_band","estress","innovation_stress","comparator_stress","innovation_no_stress","comparator_no_stress"]
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerow(dict(zip(fields, ["csv","seed","usual","site","yield","kg","RCT","severe","",850,500,1000,900])))
        self.assertEqual(self.store.import_csv(path), 1)
        self.assertEqual(self.store.rows()[0]["estress"], 250)


if __name__ == "__main__":
    unittest.main()
