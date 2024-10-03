# Review comments

This document summarizes questions and uncertainties that arose while developing
a prototype in acordance with the TIME CODE FORMATS CCSDS 301.0-P-4.1

## Comment 1

In Section 3.2, the note describes as follows:

`1. This time code is not UTC-based and leap-second corrections do not apply`

This sentence can be clarified to better reflect the intended meaning of the CUC format. The current description suggests that the CUC format only defines two things: epoch and elapsed seconds from the epoch. However, this does not fully capture the essence of the format.

A revised version of the text could read:

`1. This time code is based on UTC, but does not include leap-second corrections`

This sentence more accurately conveys that the CUC format refers to UTC as its basis, without accounting for leap seconds. This clarification will help avoid confusion and ensure consistency with practical implementations.

Furthermore, it would be beneficial to explain how to convert between the CUC format and UTC, including scenarios where leap seconds are necessary for specific use cases.

Additionally, the document should:

- Explain how to convert between CUC format and UTC, including handling of leap seconds when necessary for specific use cases.
