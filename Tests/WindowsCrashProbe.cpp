#include "HP2CrashReporter.h"
#include <windows.h>

static volatile unsigned int StackProbeSink;
__attribute__((noinline)) static void ExhaustStack(unsigned int Depth)
{
	volatile unsigned char Page[4096];
	Page[Depth % sizeof(Page)] = static_cast<unsigned char>(Depth);
	if (Depth < 1000000) ExhaustStack(Depth + 1);
	StackProbeSink += Page[Depth % sizeof(Page)];
}

int main(int argc, char** argv)
{
	SetErrorMode(SEM_NOGPFAULTERRORBOX | SEM_FAILCRITICALERRORS);
	if (argc > 1) HP2SetCrashReporterDirectory(argv[1]);
	HP2CrashReporterConfig Config = {};
	Config.ProcessName = "crash_probe";
	HP2InstallCrashReporter(&Config);
	if (argc > 2) ExhaustStack(0);
	RaiseException(0xe0424242, EXCEPTION_NONCONTINUABLE, 0, nullptr);
	return 1;
}
