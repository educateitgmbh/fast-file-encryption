# Copyright 2021 by Tobias Erbsland / EducateIT GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class IntegrityError(Exception):
    """
    This exception is thrown if there is any integrity problem with the encrypted file.

    - Wrong file magic.
    - File to short.
    - Checksum mismatch.
    - Corrupt data.
    """
    pass


class DataTooLargeError(Exception):
    """
    This exception is thrown, if you set a maximum size and it would be exceeded.
    """
    pass
