import os
import unittest
from spotty.config.abstract_instance_config import VolumeMount
from spotty.config.config_utils import _read_yaml
from spotty.config.project_config import ProjectConfig
from spotty.providers.local.config.instance_config import InstanceConfig


class TestContainerDeployment(unittest.TestCase):

    def test_instance_volume(self):
        local_project_dir = os.path.join(os.path.dirname(__file__), 'config', 'data')
        config = _read_yaml(os.path.join(local_project_dir, 'config1.yaml'))

        project_config = ProjectConfig(config, local_project_dir)
        instance_config = InstanceConfig(project_config.instances[0], project_config)

        self.assertEqual(instance_config.host_project_dir, local_project_dir)
        self.assertEqual(instance_config.dockerfile_path, os.path.join(local_project_dir, 'docker', 'Dockerfile'))
        self.assertEqual(instance_config.docker_context_path, os.path.join(local_project_dir, 'docker'))
        self.assertEqual(len(instance_config.volume_mounts), 2)
        self.assertEqual(instance_config.volume_mounts[0], VolumeMount(name='workspace',
                                                                       host_path='/mnt/test',
                                                                       mount_path='/workspace',
                                                                       mode='rw',
                                                                       hidden=False))
        self.assertEqual(instance_config.volume_mounts[1], VolumeMount(name=None,
                                                                       host_path=local_project_dir,
                                                                       mount_path='/workspace/project',
                                                                       mode='rw',
                                                                       hidden=True))


if __name__ == '__main__':
    unittest.main()
