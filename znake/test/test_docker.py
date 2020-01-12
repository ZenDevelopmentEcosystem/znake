import unittest
from unittest.mock import MagicMock, Mock, patch

from znake.docker import docker_run, get_venv_volume_name


class TestDocker(unittest.TestCase):

    @staticmethod
    def get_ctx(root=False, no_pull=False, network=None, registry=None):
        ctx = MagicMock()
        root_arg = MagicMock()
        root_arg.value = root
        no_pull_arg = MagicMock()
        no_pull_arg.value = no_pull
        network_arg = MagicMock()
        network_arg.value = network
        ctx.core.args = {
            'root': root_arg,
            'no-pull': no_pull_arg,
            'network': network_arg,
        }
        ctx.znake.docker_registry = registry
        return ctx

    def test_get_venv_volume_name(self):
        ctx = Mock()
        ctx.znake.info.package = 'my_package'
        result = get_venv_volume_name(ctx, 'my_image')
        self.assertEqual('my_package_venv_volume_my_image', result)

    def test_docker_run_without_root_flag(self):
        ctx = self.get_ctx(root=False, registry='my.docker.registry/repository')
        ctx.znake.docker.run.flags = ['--my-flag 3']
        target = {'image': 'my_image'}
        command = 'this is my command'

        with patch('znake.docker._docker_pull') as pull, patch('znake.docker._docker_run') as run:
            docker_run(ctx, target['image'], command)

        expected_image_name = 'my.docker.registry/repository/' + 'my_image'
        pull.assert_called_once_with(ctx, expected_image_name)
        run.assert_called_once_with(
            ctx,
            '--my-flag 3 --user "$(id -u):$(id -g)"',
            expected_image_name,
            command,
            interactive=False)

    def test_docker_run_with_root_flag(self):
        ctx = self.get_ctx(root=True, registry='my.docker.registry/repository')
        ctx.znake.docker.run.flags = ['--my-flag 3']
        target = {'image': 'my_image'}
        command = 'this is my command'

        with patch('znake.docker._docker_pull') as pull, patch('znake.docker._docker_run') as run:
            docker_run(ctx, target['image'], command)

        expected_image_name = 'my.docker.registry/repository/' + 'my_image'
        pull.assert_called_once_with(ctx, expected_image_name)
        run.assert_called_once_with(
            ctx, '--my-flag 3', expected_image_name, command, interactive=False)

    def test_docker_run_with_no_pull_flag(self):
        ctx = self.get_ctx(no_pull=True, registry='my.docker.registry/repository')
        ctx.znake.docker.run.flags = ['--my-flag 3']
        target = {'image': 'my_image'}
        command = 'this is my command'

        with patch('znake.docker._docker_pull') as pull, patch('znake.docker._docker_run') as run:
            docker_run(ctx, target['image'], command)

        expected_image_name = 'my.docker.registry/repository/' + 'my_image'
        pull.assert_not_called()
        run.assert_called_once_with(
            ctx,
            '--my-flag 3 --user "$(id -u):$(id -g)"',
            expected_image_name,
            command,
            interactive=False)

    def test_docker_run_with_interactive(self):
        ctx = self.get_ctx(registry='my.docker.registry/repository')
        ctx.znake.docker.run.flags = ['--my-flag 3']
        target = {'image': 'my_image'}
        command = 'this is my command'

        with patch('znake.docker._docker_pull'), patch('znake.docker._docker_run') as run:
            docker_run(ctx, target['image'], command, interactive=True)

        expected_image_name = 'my.docker.registry/repository/' + 'my_image'
        run.assert_called_once_with(
            ctx,
            '--my-flag 3 --user "$(id -u):$(id -g)" -it',
            expected_image_name,
            command,
            interactive=True)

    def test_docker_run_with_network_flag(self):
        ctx = self.get_ctx(network='network', registry='my.docker.registry/repository')
        ctx.znake.docker.run.flags = ['--my-flag 3']
        target = {'image': 'my_image'}
        command = 'this is my command'

        with patch('znake.docker._docker_pull') as pull, patch('znake.docker._docker_run') as run:
            docker_run(ctx, target['image'], command)

        expected_image_name = 'my.docker.registry/repository/' + 'my_image'
        pull.assert_called_once_with(ctx, expected_image_name)
        run.assert_called_once_with(
            ctx,
            '--my-flag 3 --user "$(id -u):$(id -g)" --network network',
            expected_image_name,
            command,
            interactive=False)

    def test_docker_run_with_no_registry_flag(self):
        ctx = self.get_ctx()
        target = {'image': 'my_image'}
        command = 'this is my command'

        with patch('znake.docker._docker_pull') as pull, patch('znake.docker._docker_run') as run:
            docker_run(ctx, target['image'], command)

        expected_image_name = 'my_image'
        pull.assert_called_once_with(ctx, expected_image_name)
        run.assert_called_once_with(
            ctx, '--user "$(id -u):$(id -g)"', expected_image_name, command, interactive=False)
