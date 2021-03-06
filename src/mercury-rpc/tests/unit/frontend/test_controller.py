# Copyright 2017 Rackspace
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import mock
import pytest

from mercury.rpc.frontend.controller import FrontEndController


@pytest.fixture()
def frontend_controller(async_mongodb):
    inventory_client = 'tcp://localhost:9000'
    jobs_collection = async_mongodb.rpc_jobs
    tasks_collection = async_mongodb.rpc_tasks
    rpc_tasks_queue = 'rpc_tasks'
    # Patch the client so we don't attempt to connect the socket
    with mock.patch('mercury.rpc.frontend.controller.InventoryClient'):
        controller = FrontEndController(inventory_client,
                                        jobs_collection,
                                        tasks_collection,
                                        'rpc_tasks')
        return controller


class TestFrontendController(object):

    @pytest.mark.asyncio
    async def test_get_job(self, frontend_controller):
        job = await frontend_controller.get_job('job-1')
        assert job.get('job_id') == 'job-1'

    @pytest.mark.asyncio
    async def test_get_job_none(self, frontend_controller):
        job = await frontend_controller.get_job('job-x')
        assert job == None
