#!/usr/bin/env python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import sys

from utils import USER_ID, USER_PASSWORD, connect_authentication_service, connect_frontend_service
from teaclave import FunctionArgument


class PolicyEnforcedDataAnalysis:

    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_password = user_password

    # Performs the data analysis with policy enforcement.
    # Since currently the framework is still under construction, the details may change.
    def analysis(self, id=0):
        with connect_authentication_service() as client:
            print("[+] login")
            token = client.user_login(self.user_id, self.user_password)

        with connect_frontend_service() as client:
            metadata = {"id": self.user_id, "token": token}
            client.metadata = metadata

            print("[+] registering function")
            function_id = client.register_function(
                name="builtin-policy-enforcement",
                description="Data Analysis with Policy Enforcement Function",
                executor_type="builtin",
                arguments=[FunctionArgument("id")])

            print("[+] creating task")
            task_id = client.create_task(
                function_id=function_id,
                function_arguments={"id": id},
                executor="builtin")

            print("[+] invoking task")
            client.invoke_task(task_id)

            print("[+] getting result")
            result = client.get_task_result(task_id)
            print("[+] done")

        return bytes(result)


def main():
    example = PolicyEnforcedDataAnalysis(USER_ID, USER_PASSWORD)
    if len(sys.argv) > 1:
        message = sys.argv[1]
        rt = example.analysis(message)
    else:
        rt = example.analysis()

    print("[+] function return: ", rt)


if __name__ == '__main__':
    main()
