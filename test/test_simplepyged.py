import unittest
import os
from simplepyged import *

class McIntyreTest(unittest.TestCase):
    """Unit tests for simplepyged.py using mcintyre.ged."""

    def setUp(self):
        self.g = Gedcom(os.path.abspath('test/mcintyre.ged'))

    def test_matches(self):
        for e in self.g.line_list():
            if e.type() == 'Individual':
                if e.surname_match('Merriman'):
                    self.assertEqual(e.name()[0], 'Lucy')
                if e.given_match('Archibald'):
                    self.assertEqual(e.name()[1], 'McIntyre')
                    self.assertEqual(e.birth_range_match(1810,1820), True)
                    self.assertEqual(e.birth_year_match(1819), True)
                if e.birth_year_match(1904):
                    self.assertEqual(e.name(), ('Carrie Lee', 'Horney'))
                    self.assertEqual(e.death_range_match(1970,1980), True)
                    self.assertEqual(e.death_year_match(1979), True)
                    self.assertEqual(e.death_year_match(1978), False)
                if e.marriage_year_match(1821):
                    if e.marriage_range_match(1820,1825):
                        if e.surname_match('McIntyre'):
                            self.assertEqual(e.name(), ('John M', 'McIntyre'))

    def test_criteria(self):
        criteria = "surname=McIntyre:birthrange=1820-1840:deathrange=1865-1870"
        for e in self.g.line_list():
            if e.type() == 'Individual':
                if e.criteria_match(criteria):
                    self.assertEqual(e.name(), ('Calvin Colin', 'McIntyre'))

        criteria = "surname=McIntyre:birth=1890:death=1953"
        for e in self.g.line_list():
            if e.type() == 'Individual':
                if e.criteria_match(criteria):
                    self.assertEqual(e.name(), ('Ernest R', 'McIntyre'))

        criteria = "surname=McIntyre:marriage=1821"
        for e in self.g.line_list():
            if e.type() == 'Individual':
                if e.criteria_match(criteria):
                    self.assertEqual(e.name(), ('John M', 'McIntyre'))

        criteria = "surname=McIntyre:marriagerange=1820-1825"
        for e in self.g.line_list():
            if e.type() == 'Individual':
                if e.criteria_match(criteria):
                    self.assertEqual(e.name(), ('John M', 'McIntyre'))


    def test_missing_xref(self):
        """I don't really know what this does..."""
        for e in self.g.line_list():
            if e.value().startswith('@'):
                f = self.g.line_dict().get(e.value(),None)
                if f == None:
                    print e.value()

        for e in self.g.line_list():
            if e.xref() == "@I99@":
                print e.name()

    def test_individuals(self):
        num_of_individuals = 0
        for e in self.g.line_list():
            if e.type() == 'Individual':
                num_of_individuals += 1

        self.assertEqual(num_of_individuals, len(self.g.individual_list()))
        self.assertEqual(num_of_individuals, len(self.g.individual_dict()))


    def test_line(self):
        """Testing class Line"""
        mary = self.g.get_individual('@P405366386@')

        self.assertEqual(mary.children_tags("SEX")[0].value(), "F")

    def test_individual(self):
        """Testing class Individual"""
        mary = self.g.get_individual('@P405366386@')

        self.assertEqual(mary.type(), 'Individual')
       
        self.assertEqual(mary.birth(), ('19 Nov 1923', 'Louisiana, USA'))
        self.assertEqual(mary.alive(), True)
        self.assertEqual(mary.father().alive(), False)
        self.assertEqual(mary.father().death(), ('19 Aug 1975', 'Bastrop, Louisiana'))
        self.assertEqual(mary.sex(), 'F')
        self.assertEqual(mary.given_name(), 'Mary Christine')
        self.assertEqual(mary.surname(), 'Hern')
        self.assertEqual(mary.fathers_name(), 'Thomas Clyde')

        self.assertEqual(mary.deceased(), False)
        self.assertEqual(mary.death(), ('', ''))
           
        self.assertEqual(mary.parent_family().xref(), '@F5@')
        self.assertEqual(mary.parent_family().husband().xref(), '@P405368888@')
        self.assertEqual(mary.father().xref(), '@P405368888@')
        self.assertEqual(mary.mother().xref(), '@P405538002@')
        self.assertEqual(map(lambda x: x.xref(), mary.families()), ['@F4@'])
        self.assertEqual(mary.father().children(), [mary])
        

class WrightTest(unittest.TestCase):
    """Unit tests for simplepyged.py using wright.ged."""

    def setUp(self):
        self.g = Gedcom(os.path.abspath('test/wright.ged'))

    def test_individual(self):
        """Testing class Individual"""
        delores = self.g.get_individual('@I294@')

        self.assertEqual(delores.type(), 'Individual')

        self.assertEqual(delores.birth(), ('24 JUL 1963', ''))
        self.assertEqual(delores.sex(), 'F')
        self.assertEqual(delores.given_name(), 'Delores')
        self.assertEqual(delores.surname(), 'Hyatt')
        self.assertEqual(delores.fathers_name(), 'HORACE')

        self.assertEqual(delores.deceased(), False)
        self.assertEqual(delores.death(), ('', ''))
           
        self.assertEqual(delores.parent_family().xref(), '@F159@')
        self.assertEqual(map(lambda x: x.xref(), delores.families()), ['@F295@'])
        self.assertEqual(delores in delores.father().children(), True)

    def test_family(self):
        family = self.g.get_family('@F1@')

        self.assertEqual(family.husband().name(), ('Cosmond G', 'Wright'))
        self.assertEqual(family.married(), True)
        self.assertEqual(family.marriage(), ('1 SEP 1973', 'Troronto, Ontario, Canada')) #sic :-)
        

if __name__ == '__main__':
    unittest.main()
