#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Takes the audio and writes the text to a text file with the samew name as the audio file

Example usage:
    python transcribe.py "audio.wav"
"""

import argparse
import io
import time

# [START speech_transcribe_sync_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    start = time.time()
    print('Waiting for operation to complete...')
    response = operation.result(timeout=3200)
    end = time.time()
    print end - start

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    output = open(gcs_uri[17:]+'.txt', 'w')
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        output.write('{}'.format(result.alternatives[0].transcript))
    output.close()
# [END speech_transcribe_sync_gcs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='GCS path for audio file to be recognized')
    args = parser.parse_args()
    transcribe_gcs('gs://audioforhtm/{}'.format(args.path))
