import re


def append_maven_repository(step_source):
    regex = r"maven\s*{\s*?url\s*[\"']https:\/\/jitpack\.io[\"']\s*}"
    correct_repositories = 'maven { url "https://packages.jetbrains.team/maven/p/academy/hyperskill-hspc" }\n' \
                           '\t\tmaven { url "https://jitpack.io" }'

    for file in step_source['hyperskill']['files']:
        if not file['name'].endswith('.gradle'):
            continue
        file['text'] = re.sub(regex, correct_repositories, file['text'])
    return step_source
