import unittest

from app.app import pull_data
from requests.exceptions import JSONDecodeError

base_url = "https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/"


class TestRequests(unittest.TestCase):

    def test_empty_input(self):
        """
        Test when nothing is concatenated to the base URL,
        exception is raised.
        """
        self.assertRaises(JSONDecodeError, pull_data, '')

    def test_wrong_input(self):
        """T
        est when wrong compound name is concatenated to the base URL,
        empty JSON is returned.
        """
        result = pull_data('aTP')
        self.assertEqual({}, result)

    def test_correct_input(self):
        """
        Test when correct compound name is concatenated to the base URL, 
        JSON in populated appropriately.
        """
        result = pull_data("ATP")
        name = result["ATP"][0]['name']
        compound = list(result.keys())[0]
        formula = result["ATP"][0]['formula']
        inchi = result["ATP"][0]['inchi']
        inchi_key = result["ATP"][0]['inchi_key']
        smiles = result["ATP"][0]['smiles']
        cross_links_count = len(result["ATP"][0]['cross_links'])

        self.assertEqual("ADENOSINE-5'-TRIPHOSPHATE", name)
        self.assertEqual("ATP", compound)
        self.assertEqual("C10 H16 N5 O13 P3", formula)
        self.assertEqual("InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(17)6(16)4(26-10)1-25-30(21,22)28-31(23,24)27-29(18,19)20/h2-4,6-7,10,16-17H,1H2,(H,21,22)(H,23,24)(H2,11,12,13)(H2,18,19,20)/t4-,6-,7-,10-/m1/s1", inchi)
        self.assertEqual("ZKHQWZAMYRWXGA-KQYNXXCUSA-N", inchi_key)
        self.assertEqual("c1nc(c2c(n1)n(cn2)C3C(C(C(O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O)O)N", smiles)
        self.assertEqual(22, cross_links_count)


if __name__ == '__main__':
    unittest.main()
