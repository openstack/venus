============================
So You Want to Contribute...
============================

For general information on contributing to OpenStack, please check out the
`contributor guide <https://docs.openstack.org/contributors/>`_ to get started.
It covers all the basics that are common to all OpenStack projects: the
accounts you need, the basics of interacting with our Gerrit review system,
how we communicate as a community, etc.

Below will cover the more project specific information you need to get started
with {{cookiecutter.service}}.

Communication
~~~~~~~~~~~~~

We use the #openstack-venus IRC channel.

The weekly meetings happen in this channel. You can find the meeting times,
previous meeting logs and proposed meeting agendas at
`Venus Team Meeting Page
<https://wiki.openstack.org/wiki/Meetings/VenusTeamMeeting>`_.

Contacting the Core Team
~~~~~~~~~~~~~~~~~~~~~~~~

The core reviewers of Venus and their emails are listed in
`Venus core team <https://review.opendev.org/admin/groups/c5c6849cdb8c46f19e2cb128686c128f36a50f60,members>`_.

New Feature Planning
~~~~~~~~~~~~~~~~~~~~

To propose or plan new features, we add a new story in the
`Venus Launchpad
<https://blueprints.launchpad.net/openstack-venus>`_
and/or propose a specification in the
`venus-specs <https://opendev.org/openstack/venus-specs>`_ repository.

Task Tracking
~~~~~~~~~~~~~

We track our tasks in the `Launchpad <https://bugs.launchpad.net/openstack-venus>`_.

If you're looking for some smaller, easier work item to pick up and get started
on, ask in the IRC meeting.

Reporting a Bug
~~~~~~~~~~~~~~~

You found an issue and want to make sure we are aware of it? You can do so on
`Launchpad <https://bugs.launchpad.net/openstack-venus/+filebug>`__.
More info about Launchpad usage can be found on `OpenStack docs page
<https://docs.openstack.org/contributors/common/task-tracking.html#launchpad>`_.

Getting Your Patch Merged
~~~~~~~~~~~~~~~~~~~~~~~~~

To merge a patch, it must pass all voting Zuul checks and get two +2s from
core reviewers. We strive to avoid scenarios where one person from a company
or organization proposes a patch, and two other core reviewers from the
same organization approve it to get it merged. In other words, at least
one among the patch author and the two approving reviewers must be from
another organization.

We are constantly striving to improve quality. Proposed patches must
generally have unit tests and/or functional tests that cover the changes,
and strive to improve code coverage.

Project Team Lead Duties
~~~~~~~~~~~~~~~~~~~~~~~~

All common PTL duties are enumerated in the `PTL guide
<https://docs.openstack.org/project-team-guide/ptl.html>`_.
