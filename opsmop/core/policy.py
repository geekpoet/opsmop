# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from opsmop.core.collection import Collection
from opsmop.core.common import memoize
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.role import Role
from opsmop.core.scope import Scope
from opsmop.facts.chaos import Chaos
from opsmop.facts.filetests import FileTests
from opsmop.facts.platform import Platform
from opsmop.facts.user_facts import UserFacts


class Policy(Collection):

    DEFAULT_DENY_FILESERVING_PATTERNS = [ '*.py', "*__pycache__*", '*.pyo', '*.pyc', '.git', '.bak', '.swp' ]

    def __init__(self, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(extra_variables=original, **common)

    def init_scope(self):
        self.set_scope(Scope.for_top_level(self))
        self.update_variables(self.variables)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, default=None),
            variables = Field(kind=dict, loader=self.set_variables),
            roles = Field(kind=list, of=Role, loader=self.set_roles)
        )

    def set_variables(self):
        return dict()
        
    def set_roles(self):
        raise Exception("Policy class must implement set_roles")

    def get_roles(self):
        return self.roles

    def get_children(self):
        return self.roles

    def allow_fileserving_paths(self):
        # "." means the directory where the policy file is.
        return [ '.' ]

    def allow_fileserving_patterns(self):
        # ex: [ '*.j2', '*.txt' ]
        return [ '*' ]

    def deny_fileserving_patterns(self):
        return self.DEFAULT_DENY_FILESERVING_PATTERNS

    @memoize
    def fact_context(self):
        return dict(
            Platform = Platform,
            FileTest = FileTests,
            UserFacts = UserFacts,
            Chaos = Chaos
        )
