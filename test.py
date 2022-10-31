from main import append_maven_repository

test_step_source = {
    'hyperskill': {
        'files': [
            {
                "name": "build.gradle",
                "placeholders": [

                ],
                "is_visible": True,
                "text": "apply plugin: 'hyperskill'\n\nsubprojects {\n    apply plugin: 'application'\n    apply plugin: 'java'\n\n    def userJava = Integer.parseInt(JavaVersion.current().getMajorVersion())\n    def hsJava = Integer.parseInt(hs.java.version)\n    def testJava = Math.max(userJava, hsJava)\n\n    java.toolchain.languageVersion = JavaLanguageVersion.of(testJava)\n\n    compileJava {\n        javaCompiler = javaToolchains.compilerFor {\n            languageVersion = JavaLanguageVersion.of(userJava)\n        }\n    }\n\n    compileTestJava {\n        javaCompiler = javaToolchains.compilerFor {\n            languageVersion = JavaLanguageVersion.of(testJava)\n        }\n    }\n\n    repositories {\n        mavenCentral()\n        maven { url \"https://jitpack.io\" }\n    }\n\n    dependencies {\n        testImplementation 'com.github.hyperskill:hs-test:release-SNAPSHOT'\n    }\n\n    configurations.all {\n        resolutionStrategy.cacheChangingModulesFor 0, 'seconds'\n    }\n\n    sourceSets {\n        main.java.srcDir 'src'\n        test.java.srcDir 'test'\n    }\n\n    test {\n        systemProperty \"file.encoding\", \"utf-8\"\n        outputs.upToDateWhen { false }\n    }\n\n    compileJava.options.encoding = 'utf-8'\n    tasks.withType(JavaCompile) {\n        options.encoding = 'utf-8'\n    }\n}\n\nproject(':util') {\n    dependencies {\n        implementation 'com.github.hyperskill:hs-test:release-SNAPSHOT'\n    }\n}\n\nconfigure(subprojects.findAll {it.name != 'util'}) {\n    dependencies {\n        testImplementation project(':util').sourceSets.main.output\n        testImplementation project(':util').sourceSets.test.output\n    }\n}\n\nwrapper {\n    gradleVersion = hs.gradle.version\n}"
            },
            {
                "name": "settings.gradle",
                "placeholders": [

                ],
                "is_visible": True,
                "text": "buildscript {\n    repositories {\n        maven { url 'https://jitpack.io' }\n    }\n\n    dependencies {\n        classpath \"com.github.hyperskill:hs-gradle-plugin:release-SNAPSHOT\"\n    }\n\n    configurations.all {\n        resolutionStrategy.cacheChangingModulesFor 0, 'seconds'\n    }\n}\n\nstatic String sanitizeName(String name) {\n    return name.replaceAll(\"[ /\\\\\\\\:<>\\\"?*|()]\", \"_\").replaceAll(\"(^[.]+)|([.]+\\$)\", \"\")\n}\n\nrootProject.projectDir.eachDirRecurse {\n    if (!isTaskDir(it) || it.path.contains(\".idea\")) {\n        return\n    }\n    def taskRelativePath = rootDir.toPath().relativize(it.toPath())\n    def parts = []\n    for (name in taskRelativePath) {\n        parts.add(sanitizeName(name.toString()))\n    }\n    def moduleName =  parts.join(\"-\")\n    include \"$moduleName\"\n    project(\":$moduleName\").projectDir = it\n}\n\ndef isTaskDir(File dir) {\n    return new File(dir, \"src\").exists() || new File(dir, \"test\").exists()\n}\n\ninclude 'util'"
            }
        ]
    }
}

changed_step_source = append_maven_repository(test_step_source)
for file in changed_step_source['hyperskill']['files']:
    print(file['text'])
