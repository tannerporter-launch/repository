/* Screenwatch launcher (macOS).
 *
 * Why this exists: Screen Recording / Accessibility permissions attach to a
 * process's code identity. A launchd job whose executable is a shell script
 * is attributed to /bin/bash — Apple's binary — so your grant never matches
 * and screencapture fails silently. This compiled binary is the app bundle's
 * main executable: it stays alive as the TCC "responsible process" and
 * spawns the capture loop as a child, which inherits the grants.
 *
 * Build:  cc -o Screenwatch.app/Contents/MacOS/screenwatch wrapper.c
 * Sign:   codesign -s - --force --identifier com.screenwatch Screenwatch.app
 * (Compile and sign ONCE, then grant permissions — re-signing invalidates
 *  existing grants.)
 */
#include <spawn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;

int main(void) {
    char script[1024];
    snprintf(script, sizeof(script), "%s/screenwatch/bin/capture-loop.sh",
             getenv("HOME") ? getenv("HOME") : "");
    char *argv[] = {"/bin/bash", script, 0};
    for (;;) {
        pid_t pid;
        int status;
        if (posix_spawn(&pid, "/bin/bash", 0, 0, argv, environ) != 0)
            return 1;
        waitpid(pid, &status, 0);
        sleep(5); /* loop crashed or exited — restart it */
    }
}
