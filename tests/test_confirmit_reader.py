import quantipy as qp
import pandas as pd
import json
from quantipy.core.tools.dp.io import read_confirmit

def test_reader():

    dataset_that_works = qp.DataSet("quantipy test data")
    dataset_that_works.read_quantipy('tests/Example Data (A).json',
                                     'tests/Example Data (A).csv')


    assert dataset_that_works.variables() == ['record_number', 'unique_id', 'age', 'birth_day', 'birth_month', 'birth_year', 'gender', 'locality', 'ethnicity', 'religion', 'q1', 'q2', 'q2b', 'q3', 'q4', 'q5.q5_grid', 'q6.q6_grid', 'q7.q7_grid', 'q8', 'q8a', 'q9', 'q9a', 'Wave', 'weight_a', 'weight_b', 'start_time', 'end_time', 'duration', 'q14_1.q14_1_grid', 'q14_2.q14_2_grid', 'q14_3.q14_3_grid', 'RecordNo']
    assert dataset_that_works.by_type().shape == (56, 9)
    assert type(dataset_that_works._data) == pd.DataFrame
    print("NOTE: This is what the dataset.meta() function should return")
    print(dataset_that_works.meta('gender'))
    print("\n\nNOTE: this is what a crosstab should look like")
    print(dataset_that_works.crosstab('q4', 'gender'))
    print("\n\nNOTE: this is what the _data object should look like")
    print(dataset_that_works._data.iloc[:,4:13].head())

    columns = set(dataset_that_works._meta['columns'].keys())
    meta_columns = set(dataset_that_works._meta['columns'].keys())
    # check that every column in the data (columns) is also in the meta
    assert columns.issubset(meta_columns)


def test_single_type():
    dataset = qp.DataSet("confirmit")
    dataset.read_confirmit('tests/confirmit_meta.json',
                           'tests/confirmit_data.json'
                            )
    # single type - no loop reference
    print(dataset.meta('q39'))
    assert dataset.crosstab('q39').shape == (3,1)
    print(dataset.meta('q21'))
    assert dataset.crosstab('q21').shape == (5,1)
    print(dataset.crosstab('q39', 'q21'))
    assert dataset.crosstab('q39', 'q21').shape == (3,5)
    # element = dataset._data.iloc[:10,22]
    # assert element[0] == 2.0
    # assert element[1] == 2.0
    # assert element[2] == 2.0
    # assert element[3] == 1.0
    # assert element[4] == 1.0
    # assert element[5] == 2.0
    # assert element[6] == 1.0
    # assert element[8] == 2.0
    # print(element)
    assert dataset.meta()['columns']['q39'] == json.loads("""
    {"name": "q39", 
    "parent": {}, 
    "type": "single", 
    "values": [
        {"text": {"en-GB": "yes"}, 
        "value": "1"},
        {"text": {"en-GB": "no"}, 
        "value": "2"}],
    "text": {"en-GB": "Use script to set values"}}""")
    # single type - with loop reference
    assert dataset.meta()['columns']['q55']['values'][1] == json.loads("""
    {"text": {"en-GB": "loopAns1"},
    "value":
    {"name": "l2",
    "parent": {},
    "type": "single",
    "values": [
        {"text": {"en-GB": "loopAns1"},
        "value": "1"},
        {"text": {"en-GB": "loopAns2"},
        "value": "2"},
        {"text": {"en-GB": "loopAns3"}, "value": "3"}],
        "text": {"en-GB": "Loop  l2 title"},
        "texts": [{"languageId": 9,
        "text": "Loop  l2 title"}],
        "variables": [{"name": "q56",
        "parent": {},
        "type": "string",
        "properties": {}}]}}""")
    
    # TODO: assert that dataset.crosstab(single) returns correct shaped
    #       dataframe
    #       assert dataset.crosstab('q39').shape == (1,1)

    # TODO: more assertions for numbers, grids etc. these can be in different
    #       test functions if that is needed

def test_delimited_set_type():
    dataset = qp.DataSet("confirmit")
    dataset.read_confirmit('tests/confirmit_meta.json',
                           'tests/confirmit_data.json')
    print(dataset.meta('q1'))
    assert dataset.meta()['columns']['q1'] == json.loads("""
    {"name": "q1",
    "parent": {},
    "type": "delimited set",
    "properties": {},
    "values": [
        {"text": {"en-GB": "ans1"}, "value": "1"},
        {"text": {"en-GB": "ans2"}, "value": "2"},
        {"text": {"en-GB": "ans3"}, "value": "3"}],
        "text": {"en-GB": "multi - default options"}}""")
    assert dataset.crosstab('q1').shape == (4,1)
    print(dataset.crosstab('q1', 'q22'))
    assert dataset.crosstab('q1', 'q22').shape == (4,5)

def test_number_type():
    dataset = qp.DataSet("confirmit")
    dataset.read_confirmit('tests/confirmit_meta.json',
                           'tests/confirmit_data.json')
    print(dataset.meta('q73'))
    print(dataset.crosstab('q73'))
    assert dataset.meta()['columns']['q73'] == json.loads("""
    {"name": "q73",
    "parent": {},
    "type": "float",
    "text": {"en-GB": "open - numeric"}}
    """)
    assert dataset.crosstab('q73').shape == (71, 1)
    assert dataset.crosstab('q73', 'q39').shape == (71, 3)
    # import pdb; pdb.set_trace()

def test_array_type():
    dataset = qp.DataSet("confirmit")
    dataset.read_confirmit('tests/confirmit_meta.json',
                           'tests/confirmit_data.json')
    print(dataset.meta()['columns']['q5_1'])
    assert dataset.crosstab('q5_1', 'q39').shape == (52, 3)
    assert dataset.meta()['masks']['q5'] == json.loads("""
    {"name": "q5",
    "parent": {},
    "type": "array",
    "properties": {},
    "items": [
        {"properties": {},
        "source": "columns@q5_1",
        "text": {"en-GB": "ans1"}},
        {"properties": {},
        "source": "columns@q5_2",
        "text": {"en-GB": "ans2"}},
        {"properties": {},
        "source": "columns@q5_3",
        "text": {"en-GB": "ans3"}}],
        "subtype": "float",
        "text": {"en-GB": "numeric list"}}""")

    assert dataset.meta()['columns']['q5_1'] == json.loads("""
    {"name": "q5_1",
    "parent": {
        "masks@q5":
        {"type": "array"}},
        "text": {"en-GB": "ans1"},
        "type": "float"}""")

    # print(dataset.to_array('my_new_grid', ['q5_2', 'q3_3', 'q4_1'], 'this is a test grid'))