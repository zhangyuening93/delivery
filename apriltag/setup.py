from distutils.core import setup, Extension

module1 = Extension('tagInfo',
					include_dirs = ['/usr/local/include','/home/yuening/Desktop/473project','/home/yuening/Desktop/473project/common'],
					library_dirs = ['/usr/local/lib','/home/yuening/Desktop/473project','/home/yuening/Desktop/473project/common'],
                    runtime_library_dirs = ['/usr/local/lib','/home/yuening/Desktop/473project','/home/yuening/Desktop/473project/common'],
                    # libraries = ['apriltag'],
                    sources = ['check_tag.c', 'getopt.c', 'homography.c','image_f32.c', 'image_u8.c','image_u32.c','matd.c','pnm.c','string_util.c','svd22.c','time_util.c','unionfind.c','workerpool.c','zarray.c','zhash.c','zmaxheap.c','apriltag.c','apriltag_quad_thresh.c','g2d.c','tag16h5.c','tag25h7.c','tag25h9.c','tag36artoolkit.c','tag36h11.c','tag36h10.c'],
                    extra_compile_args = ['-std=gnu99'],)
                    # extra_link_args = ['-lpthread -lm'])

setup (name = 'tagInfo',
       version = '1.0',
       description = 'This is a demo package',
       author = 'yuening',
       ext_modules = [module1])