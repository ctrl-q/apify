import requests

from .ApifyABC import ApifyABC


class ActorABC(ApifyABC):
    def __init__(self, actor_id, session, config):
        super().__init__(session, config)
        self._actor_id = actor_id
        self._base_url = 'https://api.apify.com/v2/acts/' + self.get_actor_id()

    def get_actor_id(self):
        """Returns: actor_id (str): actor ID"""
        return self._actor_id


class Actor(ActorABC):
    def __init__(self, actor_id, session=requests.Session(), config="apify_config.json"):
        """Class for interacting with Apify actors
        https://www.apify.com/docs/api/v2#/reference/actors

        Args:
            actor_id (str): actor ID or <username>~<actor name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(actor_id, session, config)

    def get(self):
        """Gets actor details
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/get-actor

        Returns:
            actor_details (JSON object): actor details
        """
        return super()._get()

    def update(self, settings={}):
        """Updates actor settings
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/update-actor

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new actor settings
        """
        return super()._put(data=settings)

    def delete(self):
        """Deletes the actor
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/delete-actor
        """
        return super()._delete()

    def get_list_of_versions(self):
        """Gets list of actor versions
        https://www.apify.com/docs/api/v2#/reference/actors/version-collection/get-list-of-versions

        Returns:
            version_list (JSON object): basic information about each version
        """
        url = self._base_url + "/versions"
        return super()._get(url)

    def create_version(self):
        """Creates actor version
        https://www.apify.com/docs/api/v2#/reference/actors/version-collection/create-version

        Returns:
            actor_version (JSON object): basic information about the version
        """
        url = self._base_url + "/versions"
        return super()._post(url)

    def Version(self, version_number):
        """Class for interacting with Apify actor versions
        https://www.apify.com/docs/api/v2#/reference/actors/version-object

        Args:
            version_number (str): actor version number
        Returns:
            actor_version (Actor.Version)
        """
        return _Version(self.get_actor_id(), version_number, self.get_session(), self._config)

    def get_list_of_builds(self, **kwargs):
        """Gets list of actor builds
        https://www.apify.com/docs/api/v2#/reference/actors/build-collection/get-list-of-builds

        Args:
        kwargs:
            offset (int): Rank of first build to return (default: 0)
            limit (int): Maximum number of builds to return (default: 1000)
            desc (int): If 1, builds are sorted from newest to oldest (default: None)

        Returns:
            build_list (JSON object): list of runs and their metadata
        """
        url = self._base_url + "/builds"
        return super()._get(url, None, **kwargs)

    def build(self, version, **kwargs):
        """Builds an actor
        https://www.apify.com/docs/api/v2#/reference/actors/build-collection/build-actor

        Args:
            version (str): version number to be built
        kwargs:
            useCache (bool): whether use a cache to speed up the build process (default: False)
            betaPackages (bool): whether actor is built with beta versions of Apify NPM packages
            tag (str): tag to be applied on success (default: taken from actor version's buildTag property)
            waitForFinish (int): maximum number of seconds to wait for completion (default: 0)

        Returns:
            build_list (JSON object): list of runs and their metadata
        """
        url = self._base_url + "/builds"
        kwargs["version"] = version
        return super()._post(url, None, **kwargs)

    def Build(self, build_id):
        """Class for interacting with Apify builds
        https://www.apify.com/docs/api/v2#/reference/actors/build-object

        Args:
            build_id (str): actor build ID
        Returns:
            actor_build (Actor.Build): actor build
        """
        return _Build(self.get_actor_id(), build_id, self.get_session(), self._config)

    def get_list_of_runs(self, **kwargs):
        """Gets the actor's list of runs
        https://www.apify.com/docs/api/v2#/reference/actors/run-collection/get-list-of-runs

        Args:
        kwargs:
            offset (int): Rank of first run to return (default: 0)
            limit (int): Maximum number of runs to return (default: 1000)
            desc (int): If 1, runs are sorted from newest to oldest (default: None)

        Returns:
            run_list (JSON object): list of runs and their metadata
        """
        url = self._base_url + "/runs"
        return super()._get(url, None, **kwargs)

    def run(self, input_={}, **kwargs):
        """Runs actor asynchronously
        https://www.apify.com/docs/api/v2#/reference/actors/run-collection/run-actor

        Args:
            input_ (JSON object): custom input fields (default: None)
        kwargs:
            timeout (int): timeout for the run (default: timeout from default run configuration)
            memory (int): memory limit (in MB) (default: memory from default run configuration)
            build (str): tag or number of actor build to run (default: build from default run configuration)
            waitForFinish (int): maximum number of seconds to wait for completion (default: 0)

        Returns:
            run_details (JSON object): run details
        """
        url = self._base_url + "/runs"
        return super()._post(url, input_, **kwargs)

    def run_synchronously(self, input_=None, **kwargs):
        """Runs actor and returns its output
        https://www.apify.com/docs/api/v2#/reference/actors/run-actor-synchronously

        Args:
            input_ (JSON object): custom input fields (default: None)
        kwargs:
            outputRecordKey (str): key to return from default key-value store (default: 'OUTPUT')
            timeout (int): timeout for the run (default: timeout from default run configuration)
            memory (int): memory limit (in MB) (default: memory from default run configuration)
            build (str): tag or number of actor build to run (default: build from default run configuration)

        Returns:
            out (JSON object): run output
        """
        url = self._base_url + "/run-sync"
        return super()._post(url, input_, **kwargs)

    def Run(self, run_id):
        """Class for interacting with Apify actor runs
        https://www.apify.com/docs/api/v2#/reference/actors/run-object

        Args:
            run_number (str): actor version number
        Returns:
            actor_run (Actor.Run): actor run
        """
        return _Run(self.get_actor_id(), run_id, self.get_session(), self._config)


class Task(ApifyABC):
    def __init__(self, task_id, session=requests.Session(), config="apify_config.json"):
        """Class for interacting with Apify actor tasks
        https://www.apify.com/docs/api/v2#/reference/actor-tasks

        Args:
            task_id (str): actor ID or <username>~<actor name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(session, config)
        self._task_id = task_id
        self._base_url = 'https://api.apify.com/v2/actor-tasks/' + self.get_task_id()

    def get_task_id(self):
        """Returns: task_id (str): actor task ID"""
        return self._task_id

    def get(self):
        """Gets task details
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/task-object/get-task

        Returns:
            task_details (JSON object): actor details
        """
        return super()._get()

    def update(self, settings={}):
        """Updates task settings
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/task-object/update-task

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new task settings
        """
        return super()._put(data=settings)

    def delete(self):
        """Deletes the task
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/task-object/delete-task
        """
        return super()._delete()

    def get_list_of_runs(self, **kwargs):
        """Gets the task's list of runs
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/runs-collection/get-a-list-of-runs

        Args:
        kwargs:
            offset (int): Rank of first run to return (default: 0)
            limit (int): Maximum number of runs to return (default: 1000)
            desc (int): If 1, runs are sorted from newest to oldest (default: None)

        Returns:
            run_list (JSON object): list of runs and their metadata
        """
        url = self._base_url + "/runs"
        return super()._get(url, None, **kwargs)

    def run_asynchronously(self, input_={}, **kwargs):
        """Runs task and returns run details
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/runs-collection/run-task-asynchronously

        Args:
            input_ (JSON object): custom input fields (default: None)
        kwargs:
            waitForFinish (int): maximum number of seconds to wait for completion (default: 0)

        Returns:
            actor_run_details (JSON object): actor run details
        """
        url = self._base_url + "/runs"
        return super()._post(url, input_, **kwargs)

    def run_synchronously(self, input_={}, **kwargs):
        """Runs task and returns its output
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/run-task-synchronously/run-task-synchronously

        Args:
            input_ (JSON object): custom input fields (default: None)
        kwargs:
            outputRecordKey (str): key to return from default key-value store (default: 'OUTPUT')

        Returns:
            out (JSON object): run output
        """
        url = self._base_url + "/run-sync"
        return super()._get(url, input_, **kwargs)


class _Build(ActorABC):
    def __init__(self, actor_id, build_id, session, config):
        super().__init__(actor_id, session, config)
        self._build_id = build_id
        self._base_url += "/builds/" + self.get_build_id()

    def get_build_id(self):
        """Returns: version_number (str): actor version number"""
        return self._build_id

    def get(self, **kwargs):
        """Gets actor build details
        https://www.apify.com/docs/api/v2#/reference/actors/build-object/get-build

        Args:
        kwargs:
            waitForFinish (int): maximum number of seconds to wait for completion (default: 0)

        Returns:
            actor_build_details (JSON object): actor build details
        """
        return super()._get(None, None, **kwargs)

    def abort(self):
        url = self._base_url.replace(self.get_build_id(), "abort" + self.get_build_id())
        return super()._post(url)


class _Run(ActorABC):
    def __init__(self, actor_id, run_id, session, config):
        super().__init__(actor_id, session, config)
        self._run_id = run_id
        self._base_url += "/runs/" + self.get_run_id()

    def get_run_id(self):
        """Returns: run_id (str): actor run ID"""
        return self._run_id

    def get(self, **kwargs):
        """Gets actor run details
        https://www.apify.com/docs/api/v2#/reference/actors/run-object/get-run

        Args:
        kwargs:
            waitForFinish (int): maximum number of seconds to wait for completion (default: 0)
        Returns:
            actor_run_details (JSON object): actor run details
        """
        return super()._get(None, None, **kwargs)

    def abort(self):
        """Aborts actor run
        https://www.apify.com/docs/api/v2#/reference/actors/abort-run/abort-run

        Returns:
            actor_run_details (JSON object): actor run details
        """
        url = self._base_url.replace(self.get_run_id(), "abort" + self.get_run_id())
        return super()._post(url)


class _Version(ActorABC):
    def __init__(self, actor_id, version_number, session, config):
        super().__init__(actor_id, session, config)
        self._version_number = version_number
        self._base_url += "/versions/" + self.get_version_number()

    def get_version_number(self):
        """Returns: version_number (str): actor version number"""
        return self._version_number

    def get(self):
        """Gets actor version details
        https://www.apify.com/docs/api/v2#/reference/actors/version-object/get-version

        Returns:
            actor_version_details (JSON object): actor version details
        """
        return super()._get()

    def update(self, settings={}):
        """Updates actor version settings
        https://www.apify.com/docs/api/v2#/reference/actors/version-object/update-version

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new actor version settings
        """
        return super()._put(data=settings)

    def delete(self):
        """Deletes the actor version
        https://www.apify.com/docs/api/v2#/reference/actors/version-object/delete-version
        """
        return super()._delete()
