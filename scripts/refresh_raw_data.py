# Copyright 2014 Allen Institute for Brain Science
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Nicholas Cain
# Allen Institute for Brain Science
# June 11 2014
# nicholasc@alleninstitute.org

import requests
import os
import zipfile
import shutil

# Settings:
data_dir='../data_all'
file_save_dir = os.path.join(data_dir,'raw_data')
experiment_list_file_name = '../data_all/LIMS_id_list.p' 

# Get list of experiments:
if os.path.isfile(experiment_list_file_name):
    from friday_harbor.utilities import unpickle
    LIMS_id_list = unpickle(experiment_list_file_name)
else:
    from friday_harbor.experiment import ExperimentManager
    EM=ExperimentManager(data_dir)
    ex_list=EM.wildtype()
    LIMS_id_list=[ex.id for ex in ex_list]
    
for curr_LIMS_id in LIMS_id_list:
    # Initializations:
    file_name = os.path.join(file_save_dir, 'experiment_%s.zip' % curr_LIMS_id)
    experiment_info_url = 'http://api.brain-map.org/grid_data/download/%s?include=density,injection' % curr_LIMS_id
    
    # Get data:
    with open(file_name,'wb') as handle:
        request = requests.get(experiment_info_url, stream=True)
        for block in request.iter_content(1024):
            if not block:
                break
            handle.write(block)
    handle.close()
    
    # Unzip:
    unzip_path = os.path.join(file_save_dir, '%s' % curr_LIMS_id)
    shutil.rmtree(unzip_path, unzip_path)
    os.mkdir(unzip_path)
    zf = zipfile.ZipFile(file_name, 'r')
    zf.extractall(unzip_path)
    zf.close()
    os.remove(file_name)
    print file_name
    
