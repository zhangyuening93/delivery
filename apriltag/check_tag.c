#include <Python.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <ctype.h>
#include <unistd.h>
#include <math.h>

#include "apriltag.h"
#include "image_u8.h"
#include "tag36h11.h"
#include "tag36h10.h"
#include "tag36artoolkit.h"
#include "tag25h9.h"
#include "tag25h7.h"

#include "zarray.h"
#include "getopt.h"

#define PI 3.14159265

// Invoke:
//
// tagtest [options] input.pnm

static PyObject *TagError;

int CheckTag_system(float* c_1, float* c_2,float* angle, int argc, char *argv[])
{
    int retVal=0;

    getopt_t *getopt = getopt_create();

    getopt_add_bool(getopt, 'h', "help", 0, "Show this help");
    getopt_add_bool(getopt, 'd', "debug", 0, "Enable debugging output (slow)");
    getopt_add_bool(getopt, 'q', "quiet", 0, "Reduce output");
    getopt_add_string(getopt, 'f', "family", "tag36h11", "Tag family to use");
    getopt_add_int(getopt, '\0', "border", "1", "Set tag family border size");
    getopt_add_int(getopt, 'i', "iters", "1", "Repeat processing on input set this many times");
    getopt_add_int(getopt, 't', "threads", "4", "Use this many CPU threads");
    getopt_add_double(getopt, 'x', "decimate", "1.0", "Decimate input image by this factor");
    getopt_add_double(getopt, 'b', "blur", "0.0", "Apply low-pass blur to input");
    getopt_add_bool(getopt, '0', "refine-edges", 1, "Spend more time trying to align edges of tags");
    getopt_add_bool(getopt, '1', "refine-decode", 0, "Spend more time trying to decode tags");
    getopt_add_bool(getopt, '2', "refine-pose", 0, "Spend more time trying to precisely localize tags");

    if (!getopt_parse(getopt, argc, argv, 1) || getopt_get_bool(getopt, "help")) {
        printf("Usage: %s [options] <input files>\n", argv[0]);
        getopt_do_usage(getopt);
        exit(0);
    }

    const zarray_t *inputs = getopt_get_extra_args(getopt);

    apriltag_family_t *tf = NULL;
    const char *famname = getopt_get_string(getopt, "family");
    if (!strcmp(famname, "tag36h11")){
        tf = tag36h11_create();
        // printf("I am in! yEs\n");        
    }
    else if (!strcmp(famname, "tag36h10"))
        tf = tag36h10_create();
    else if (!strcmp(famname, "tag36artoolkit"))
        tf = tag36artoolkit_create();
    else if (!strcmp(famname, "tag25h9"))
        tf = tag25h9_create();
    else if (!strcmp(famname, "tag25h7"))
        tf = tag25h7_create();
    else {
        printf("Unrecognized tag family name. Use e.g. \"tag36h11\".\n");
        exit(-1);
    }

    tf->black_border = getopt_get_int(getopt, "border");

    apriltag_detector_t *td = apriltag_detector_create();
    if (tf == NULL){
        // printf("No way!!\n");
    }
    apriltag_detector_add_family(td, tf);
    td->quad_decimate = getopt_get_double(getopt, "decimate");
    td->quad_sigma = getopt_get_double(getopt, "blur");
    td->nthreads = getopt_get_int(getopt, "threads");
    td->debug = getopt_get_bool(getopt, "debug");
    td->refine_edges = getopt_get_bool(getopt, "refine-edges");
    td->refine_decode = getopt_get_bool(getopt, "refine-decode");
    td->refine_pose = getopt_get_bool(getopt, "refine-pose");

    int quiet = getopt_get_bool(getopt, "quiet");

    int maxiters = getopt_get_int(getopt, "iters");

    const int hamm_hist_max = 10;

    for (int iter = 0; iter < maxiters; iter++) {

        // if (maxiters > 1)
        //     printf("iter %d / %d\n", iter + 1, maxiters);

        for (int input = 0; input < zarray_size(inputs); input++) {

            int hamm_hist[hamm_hist_max];
            memset(hamm_hist, 0, sizeof(hamm_hist));

            char *path;
            zarray_get(inputs, input, &path);
            // if (!quiet)
            //     printf("loading %s\n", path);

            image_u8_t *im = image_u8_create_from_pnm(path);
            // printf("Am I wron\n");
            if (im == NULL) {
                printf("couldn't find %s\n", path);
                continue;
            }

            zarray_t *detections = apriltag_detector_detect(td, im);

            // printf("need to check\n");
            for (int i = 0; i < zarray_size(detections); i++) {
                // printf("so i am not in\n");
                apriltag_detection_t *det;
                zarray_get(detections, i, &det);

                if (!quiet){
                    retVal = det->id;
                    *angle = atan2((det->p[1][1]-det->p[0][1]),(det->p[1][0]-det->p[0][0]))/PI*180;
                    *c_1 = det->c[0];
                    *c_2 = det->c[1];
                    // printf("detection %3d: id (%2dx%2d)-%-4d, hamming %d, goodness %8.3f, margin %8.3f\n, center: %5.2f,%5.2f, angle: %5.2f, \ncorner: %5.2f, %5.2f,\n%5.2f,%5.2f,\n%5.2f,%5.2f,\n%5.2f,%5.2f,\n",
                    //        i, det->family->d*det->family->d, det->family->h, det->id, det->hamming, det->goodness, det->decision_margin,
                    //        det->c[0],det->c[1],atan2((det->p[1][1]-det->p[0][1]),(det->p[1][0]-det->p[0][0]))/PI*180,det->p[0][0],det->p[0][1],det->p[1][0],det->p[1][1],det->p[2][0],det->p[2][1],det->p[3][0],det->p[3][1]);
                }

                hamm_hist[det->hamming]++;
            }

            apriltag_detections_destroy(detections);

            // if (!quiet) {
            //     timeprofile_display(td->tp);
            //     printf("nedges: %d, nsegments: %d, nquads: %d\n", td->nedges, td->nsegments, td->nquads);
            // }

            // if (!quiet)
            //     printf("Hamming histogram: ");

            // for (int i = 0; i < hamm_hist_max; i++)
            //     printf("%5d", hamm_hist[i]);

            // if (quiet) {
            //     printf("%12.3f", timeprofile_total_utime(td->tp) / 1.0E3);
            // }

            // printf("\n");

            image_u8_destroy(im);
        }
    }

    // don't deallocate contents of inputs; those are the argv
    apriltag_detector_destroy(td);

    tag36h11_destroy(tf);
    return retVal;
}


int CheckTag_helper(float* c_1, float* c_2,float* angle, const char *command){
    int argcVal = 2;
    int retVal = 0;
    char *argv[2] = {"hello", command};
    // printf("Yes\n");
    retVal = CheckTag_system(c_1, c_2, angle, argcVal, argv);
    // printf("Yes\n");
    return retVal;
}


static PyObject *
tag_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;
    float c_1;
    float c_2;
    float angle;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = CheckTag_helper(&c_1, &c_2, &angle, command);
    if (sts < 0) {
        PyErr_SetString(TagError, "System command failed");
        return NULL;
    }
    return Py_BuildValue("[ifff]", sts, c_1, c_2, angle);
}

static PyMethodDef TagMethods[] ={
    {"tagInfo", tag_system, METH_VARARGS, "return tag info"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
inittagInfo(void)
{
    PyObject *m;

    m = Py_InitModule("tagInfo", TagMethods);
    if (m == NULL)
        return;

    TagError = PyErr_NewException("tag.error", NULL, NULL);
    Py_INCREF(TagError);
    PyModule_AddObject(m, "error", TagError);
}