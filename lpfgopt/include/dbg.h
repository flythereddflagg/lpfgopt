/*
Zed A. Shaw's Awesome Debug Macros
Annotated by Mark Redd
*/

#ifndef __dbg_h__
#define __dbg_h__
#ifndef SUPPRESS_MSG

#include <stdio.h>
#include <errno.h>
#include <string.h>

#define err_out(B, M, ...) fprintf(B, M, ...)

#else 
#define err_out(B, M, ...)
#endif

#ifdef NDEBUG
    #define debug(M, ...)
#else
    #define debug(M, ...) err_out(stderr,\
        "[C DEBUG] %s:%d: in_function: %s) " M "\n",\
        __FILE__, __LINE__, __FUNCTION__, ##__VA_ARGS__)
#endif

#define clean_errno() (errno == 0 ? "None" : strerror(errno))

#define log_err(M, ...) err_out(stderr,\
    "[C ERROR] (%s:%d: in_function: %s errno: %s) " M "\n",\
    __FILE__, __LINE__, __FUNCTION__, clean_errno(), ##__VA_ARGS__)

#define log_warn(M, ...) err_out(stderr,\
    "[C WARN] (%s:%d: in_function: %s errno: %s) " M "\n",\
    __FILE__, __LINE__, __FUNCTION__, clean_errno(), ##__VA_ARGS__)

#define log_info(M, ...) err_out(stderr,\
    "[C INFO] (%s:%d: in_function: %s ) " M "\n",\
    __FILE__, __LINE__, __FUNCTION__, ##__VA_ARGS__)

#define check(A, M, ...) if(!(A)) { log_err(M, ##__VA_ARGS__);\
    errno=0; goto error; }

#define sentinel(M, ...) { log_err(M, ##__VA_ARGS__);\
    errno=0; goto error; }

#define check_mem(A) check((A), "Out of memory.")

#define check_debug(A, M, ...) if(!(A)) { debug(M, ##__VA_ARGS__);\
    errno=0; goto error; }

#endif