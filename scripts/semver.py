#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Strict SemVer 2.0 parsing and precedence for protocol validators."""

from __future__ import annotations

import re
from dataclasses import dataclass


SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


@dataclass(frozen=True)
class SemVer:
    """A parsed SemVer value whose comparison method implements precedence only."""

    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...] = ()
    build: tuple[str, ...] = ()

    @classmethod
    def parse(cls, value: str) -> "SemVer":
        if not isinstance(value, str):
            raise ValueError(f"semantic version must be a string: {value!r}")
        match = SEMVER_RE.fullmatch(value)
        if match is None:
            raise ValueError(f"invalid semantic version: {value!r}")

        prerelease = tuple(match.group(4).split(".")) if match.group(4) else ()
        for identifier in prerelease:
            if identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"):
                raise ValueError(
                    "numeric prerelease identifiers must not contain leading zeroes: "
                    f"{value!r}"
                )

        build = tuple(match.group(5).split(".")) if match.group(5) else ()
        return cls(
            major=int(match.group(1)),
            minor=int(match.group(2)),
            patch=int(match.group(3)),
            prerelease=prerelease,
            build=build,
        )

    def compare_precedence(self, other: "SemVer") -> int:
        """Return -1, 0, or 1 according to SemVer 2.0 precedence rules."""
        left_core = (self.major, self.minor, self.patch)
        right_core = (other.major, other.minor, other.patch)
        if left_core != right_core:
            return -1 if left_core < right_core else 1

        if not self.prerelease and not other.prerelease:
            return 0
        if not self.prerelease:
            return 1
        if not other.prerelease:
            return -1

        for left, right in zip(self.prerelease, other.prerelease):
            if left == right:
                continue
            left_numeric = left.isdigit()
            right_numeric = right.isdigit()
            if left_numeric and right_numeric:
                return -1 if int(left) < int(right) else 1
            if left_numeric != right_numeric:
                return -1 if left_numeric else 1
            return -1 if left < right else 1

        if len(self.prerelease) == len(other.prerelease):
            return 0
        return -1 if len(self.prerelease) < len(other.prerelease) else 1


def compare_semver(left: str, right: str) -> int:
    """Compare two SemVer strings by precedence; build metadata is ignored."""
    return SemVer.parse(left).compare_precedence(SemVer.parse(right))
