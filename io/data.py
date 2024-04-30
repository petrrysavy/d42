import pandas as pd
from io.sample import Sample


class Data:
    def __init__(self, samples, variables_annotation=None):
        """
        Initialize Data with a list of samples.

        Parameters:
        samples (list): List of Sample objects.
        """
        if variables_annotation is None:
            variables_annotation = {}
        self._list = samples
        self._variables_annotation = variables_annotation

    def add_sample(self, sample):
        """
        Add a sample to the list of samples.

        Parameters:
        sample (Sample): Sample object to add.
        """
        self._list.add(sample)

    def add_annotation(self, variable, *annotations):
        """
        Adds a new annotations to the variable.
        :param variable: Variable that should be annotated.
        :param annotations: Properties of the variable. See variableannotation module.
        """
        annot_set = self._variables_annotation.get(variable, set())
        for annotation in annotations:
            annot_set.add(annotation)

    def get_annotations(self, variable):
        """
        Returns unmodifiable view of the annotations of a variable.
        :param variable: Variable to query.
        :return: A set of annotations.
        """
        annotations = self._variables_annotation.get(variable, set())
        return frozenset(annotations)

    def get_dynamic_variables(self):
        """
        Returns a set of all dynamic variables.
        :return: List of dynamic variables.
        """
        variables = set()
        for sample in self._list:
            variables = variables.union(sample._data.columns)
        return variables

    def get_common_dynamic_variables(self):
        """
        Returns a set of dynamic variables that are stored among all samples.
        :return: List of dynamic variables.
        """
        variables = set()
        for sample in self._list:
            variables = variables.intersection(sample._data.columns)
        return variables

    def project(self, variables):
        """
        Returns a view on selected variables.
        :param variables: Variables to project.
        :return: A new dataset that contains only selected variables.
        """
        return Data([sample.project(variables) for sample in self._list], variables_annotation=self._variables_annotation)

    def dynamic_variables(self):
        """
        Returns a list of pandas data frames with dynamic variables.
        :return: List of pandas data frames.
        """
        return [sample.get_data() for sample in self._list]


    def __iter__(self):
        """
        Make the Data object iterable.

        Returns:
        iterator: Iterator over the list of samples.
        """
        return iter(self._list)

