from __future__ import annotations

import itertools
from collections import OrderedDict, defaultdict
from typing import Optional

import numpy as np
import pandas as pd

import cellranger.matrix as cr_matrix
import cellranger.rna.library as rna_library
import tenkit.stats as tk_stats
from cellranger.analysis.combinatorics import generate_solutions, multinomial_comb
from cellranger.feature.feature_assignments import CellsPerFeature, FeatureAssignmentsMatrix
from cellranger.feature.throughputs import CORR_FACTOR, N_G
from cellranger.pandas_utils import sanitize_dataframe

def my_assign_features(self):
    assignments: OrderedDict[bytes, FeatureAssignmentsMatrix] = OrderedDict()
    feature_ids_this_type = self.matrix.get_feature_ids_by_type(self.feature_type)

    for feature_id in feature_ids_this_type:
        assert isinstance(feature_id, bytes)
        umi_counts = self.matrix.get_subselected_counts(
            log_transform=False, library_type=self.feature_type, list_feature_ids=[feature_id]
        )

        in_high_umi_component = self._call_presence(umi_counts, self.method)
        assignments[feature_id] = FeatureAssignmentsMatrix(
            np.flatnonzero(np.array(in_high_umi_component)), sum(umi_counts), False, []
        )

    # assignments = self.identify_contaminant_tags(assignments)

    return assignments

cellranger.feature.feature_assigner.FeatureAssigner.assign_features = my_assign_features