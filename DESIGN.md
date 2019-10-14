# Docker API Test

## Goal
I aim to accurately demonstrate my engineering abilities, and learn about
what Gravitational values in engineering, QA, and code review.  As a
secondary goal, we're going to accomplish this by collaborating on "a single
black-box test for Docker API running on the local host on Linux machine."

The ideal outcome is that both the Gravititational Interview Team and I figure
out if we want to work with each other.

## Overview
I aim to write a single [functional](https://en.wikipedia.org/wiki/Functional_testing)
test that non-exhaustively exercises the Docker daemon's start, stop and logs
API endpoints throughout a well-known container's brief life-cycle.

The test will developed Python 3 v3.6.8 without any 3rd-party test harness
(e.g. pytest, nosetests) or 3rd-party docker client APIs.

## Design Goals
* Limit scope such that it is reasonable to accomplish the goals (and review
the project) in <=8 hours + some design/research time the day before.
* Aim to have interviewers running the test with as little manual setup and
headache as possible.
* Consistent, structured & professional code and CR interactions.
  * For Python I choose to follow [flake8](http://flake8.pycqa.org/en/latest/)
default settings, except for max-line-length.
* Reproducible builds.

## In Scope
* A single fuctional test.
* Exercising following 3 docker API endpoints, in the following order:
  * POST /containers/&lt;id&gt;/start
  * POST /containers/&lt;id&gt;/stop
  * GET /containers/&lt;id&gt;/logs
* Give robust and useful errors considering the following daemon issues:
  * The docker daemon is not running when the test begins.
  * The docker daemon is killed or forced to hang during test execution.
   (Although not in the doc, Sasha all but stated this would happen)
* Bootstrap automation to ease running the test. (E.g. loading the well-known
image into docker or expected cleanup for idempotency before/after a test run)


## Out of Scope
* Testing anything that requires network calls beyond the Linux host. For
example fetching a container from the general registry.
  * Why: Crossing the network boundary (especially to the internet) is an
enormous source of non-determinism we don't want to introduce into a test --
especially if this were to be used as a regression test.
* Exercising docker authentication is [out of scope](https://getgravity.slack.com/archives/GPD552ALE/p1571082899008900).
The user running the test is expected to be able to issue calls with to the
docker daemon with no code configuration.
* [The Interview team has their own solution for provisioing test sandboxes](https://getgravity.slack.com/archives/GPD552ALE/p1571082456004500).
I chose to use Vagrant for my own sake.
* Handling any users/processes simultaneously using docker in the test sandbox
(except for the specific daemon shenanigans mentioned above) is out of scope.
  * Why: Unless we're doing stress/fuzz testing, multiple processes banging on the
same test subject is indicative of poor test isolation and a source of
nondeterminism.
* Any sort of scheduling/job harness/machine interop is
[out of scope for now](https://getgravity.slack.com/archives/GPD552ALE/p1571082891008600).
The test is expected to be invoked by a human, and the results interpreted by
a human.
* Multiple/diverse containers. Why: Unnecessary for MVP.
