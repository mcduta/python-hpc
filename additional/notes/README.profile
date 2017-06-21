https://www.ibm.com/developerworks/community/blogs/jfp/entry/Python_Meets_Julia_Micro_Performance?lang=en

Can we do more?  One way to know is to profile the code.  The built-in %prun profiler is not precise enough here, and we must use a better profiler known as line_profiler.  It can be installed via pip:

pip install line_profiler

Once installed, we load it:

    %load_ext line_profiler

We can then profile the function using a magic:

    %lprun -s -f mandelperf_numba mandelperf_numba()

