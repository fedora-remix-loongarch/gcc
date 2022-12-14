#!/usr/bin/env bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Regression/bz1960701-Wrong-code-regression-starting-with-gcc-8-2
#   Description: Test for BZ#1960701 (Wrong-code regression starting with gcc 8.2)
#   Author: Vaclav Kadlcik <vkadlcik@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2021 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

# Notes on relevancy
#
# The test is applicable to GCCs supporting -std=c++17. In practice,
#   * any supported toolset GCC
#   * system GCC of RHEL 8+; however the respective fix landed in 8.5
#     and isn't planned for backporting.
#
# Suggested TCMS relevancy:
#   distro < rhel-8 && collection !defined: False
#   distro < rhel-8.5 && collection !defined: False

GCC="${GCC:-$(type -P gcc)}"
PACKAGE=$(rpm --qf '%{name}\n' -qf $GCC | head -1)
PACKAGES="${PACKAGE} ${PACKAGE}-c++"

rlJournalStart
    rlPhaseStartSetup
        rlLogInfo "PACKAGES=$PACKAGES"
        rlLogInfo "COLLECTIONS=$COLLECTIONS"
        rlAssertRpm --all
        rlRun "TmpDir=\$(mktemp -d)"
        rlRun "cp reproducer.cc $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun 'g++ -o reproducer -Wall -Wextra -std=c++17 reproducer.cc'
        rlRun './reproducer'
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun 'popd'
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
