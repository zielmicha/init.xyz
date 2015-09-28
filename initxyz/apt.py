from subprocess import check_output, check_call
from collections import namedtuple
from .session import SessionPlugin
from .utils import cached_property

Package = namedtuple('Package', 'name architecture')

class Apt:
    @cached_property
    def package_list(self):
        cmd = ['dpkg-query', '-f', '${binary:Package}\n', '-W']
        result = []
        for line in check_output(cmd).decode('utf-8').splitlines():
            result.append(self.package_from_name(line))

        return result

    def package_from_name(self, name):
        if ':' in name:
            name, arch = name.rsplit(':', 1)
        else:
            name = name
            arch = self.primary_architecture

        return Package(name, arch)

    @cached_property
    def primary_architecture(self):
        return check_output(['dpkg', '--print-architecture']).decode('utf-8').strip()

    @cached_property
    def foreign_architectures(self):
        return check_output(['dpkg', '--print-foreign-architectures']).decode('utf-8').splitlines()

    def require_architecture(self, *names):
        for name in names:
            if name != self.primary_architecture and name not in self.foreign_architectures:
                check_call(['sudo', 'dpkg', '--add-architecture', name])
                check_call(['sudo', 'apt-get', 'update'])

    def require(self, *names):
        not_installed = list(filter(lambda name: not self.is_installed(name), names))
        if not_installed:
            check_call(['sudo', 'apt-get', 'install', '--yes'] + not_installed)

    def is_installed(self, pkg_name):
        return self.package_from_name(pkg_name) in self.package_list

apt = Apt()
