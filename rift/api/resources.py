"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import uuid
import falcon

from rift.api.common.resources import ApiResource
from rift.data.model import (build_job_from_dict, get_job, get_jobs, save_job)
from rift.actions import execute_job


class JobsResource(ApiResource):

    def on_post(self, req, resp, tenant_id):
        body = self.load_body(req)
        body['tenant_id'] = tenant_id
        body['job_id'] = str(uuid.uuid4())
        job = build_job_from_dict(body)
        save_job(job)
        execute_job.delay(job.job_id)
        resp.status = falcon.HTTP_201

    def on_get(self, req, resp, tenant_id):
        jobs = get_jobs(tenant_id)
        resp.body = self.format_response_body([job.as_dict() for job in jobs])



class GetJobResource(ApiResource):

    def on_get(self, req, resp, tenant_id, job_id):
        job = get_job(job_id)
        if job:
            resp.body = self.format_response_body(job.as_dict())
        else:
            resp.status = falcon.HTTP_404
            resp.body = 'Cannot find job: {job_id}'.format(job_id=job_id)
