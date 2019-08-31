# lscpu： #

	~]# lscpu 
	Architecture:          x86_64
	CPU op-mode(s):        32-bit, 64-bit
	Byte Order:            Little Endian
	CPU(s):                1
	On-line CPU(s) list:   0
	Thread(s) per core:    1
	Core(s) per socket:    1
	Socket(s):             1
	NUMA node(s):          1
	Vendor ID:             GenuineIntel
	CPU family:            6
	Model:                 60
	Model name:            Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz
	Stepping:              3
	CPU MHz:               3192.669
	BogoMIPS:              6385.33
	Virtualization:        VT-x
	Hypervisor vendor:     VMware
	Virtualization type:   full
	L1d cache:             32K
	L1i cache:             32K
	L2 cache:              256K
	L3 cache:              6144K
	NUMA node0 CPU(s):     0
	Flags:                 ...


	Socket(s):             1		#表示一个物理CPU
	Core(s) per socket:    1		#一个物理CPU上有一个核心
	Thread(s) per core:    1		#每个核心上有一个线程（超线程）

# CPU info： #

	~]# cat /proc/cpuinfo 
		processor       : 0
		vendor_id       : GenuineIntel
		cpu family      : 6
		model           : 60
		model name      : Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz
		stepping        : 3
		microcode       : 0x19
		cpu MHz         : 3192.669
		cache size      : 6144 KB
		physical id     : 0
		siblings        : 1
		core id         : 0
		cpu cores       : 1
		apicid          : 0
		initial apicid  : 0
		fpu             : yes
		fpu_exception   : yes
		cpuid level     : 13
		wp              : yes
		flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon nopl xtopology tsc_reliable nonstop_tsc eagerfpu pni pclmulqdq vmx ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm tpr_shadow vnmi ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 invpcid xsaveopt arat
		bogomips        : 6385.33
		clflush size    : 64
		cache_alignment : 64
		address sizes   : 43 bits physical, 48 bits virtual
		power management:

	注：
		1.同一个socket的physical id相同
		2.cpu cores表示此socket上的core数量
		3.如果cpu cores = siblings，表明没有开启超线程
		4.如果cpu cores = 2 * siblings，表明开启了超线程
		5.相同的physical id，相同的core id，但是不同的processor，表明是同一个core上的逻辑CPU（超线程）