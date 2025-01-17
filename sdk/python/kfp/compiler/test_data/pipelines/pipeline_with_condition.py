# Copyright 2021 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kfp import compiler
from kfp import components
from kfp import dsl
from kfp.dsl import component


@component
def flip_coin_op() -> str:
    """Flip a coin and output heads or tails randomly."""
    import random
    result = 'heads' if random.randint(0, 1) == 0 else 'tails'
    return result


@component
def print_op(msg: str):
    """Print a message."""
    print(msg)


@dsl.pipeline(name='single-condition-pipeline', pipeline_root='dummy_root')
def my_pipeline(text: str = 'condition test'):
    flip1 = flip_coin_op().set_caching_options(False)
    print_op(msg=flip1.output)

    with dsl.Condition(flip1.output == 'heads'):
        flip2 = flip_coin_op().set_caching_options(False)
        print_op(msg=flip2.output)
        print_op(msg=text)


if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=my_pipeline,
        package_path=__file__.replace('.py', '.yaml'))
