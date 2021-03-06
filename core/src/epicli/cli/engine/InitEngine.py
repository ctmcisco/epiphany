
import os

from cli.helpers.Step import Step
from cli.helpers.build_saver import save_manifest, get_build_path
from cli.helpers.data_loader import load_all_yaml_objs, types, load_all_documents_from_folder
from cli.engine.BuildEngine import BuildEngine
from cli.version import VERSION


class InitEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.provider = input_data.provider
        self.full_config = input_data.full_config
        self.name = input_data.name
        self.is_full_config = input_data.full_config

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)  

    def init(self):
        defaults = load_all_yaml_objs(types.DEFAULT, self.provider, 'configuration/minimal-cluster-config')
        defaults[0].specification.name = self.name

        for i in range(len(defaults)): 
            defaults[i]['version'] = VERSION       

        if self.is_full_config:
            defaults = self.get_full_config(defaults)

        save_manifest(defaults, self.name, self.name+'.yml')

        self.logger.info('Initialized user configuration and saved it to "' + os.path.join(get_build_path(self.name), self.name + '.yml') + '"')
        return 0

    def get_full_config(self, config_docs):
        cluster_config_path = save_manifest(config_docs, self.name, self.name + '.yml')
        args = type('obj', (object,), {'file': cluster_config_path})()
        with BuildEngine(args) as build:
            docs = build.dry_run()

        # set the provider for all docs
        for doc in docs:
            if 'provider' not in doc.keys():
                doc['provider'] = self.provider

        return docs





