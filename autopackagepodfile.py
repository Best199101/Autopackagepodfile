#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import re
import time


framkework_Satus = raw_input('请选择framework打包类型1真机版本,2模拟器版本,3聚合版本:')

current_path = os.getcwd()
super_path = os.path.abspath(os.path.join(os.getcwd(), ".."))

project_path = current_path
podfile_path = project_path + '/Podfile'
workspace_name = 'G_OSLib'
build_path = project_path + '/DerivedData'
product_path = super_path + '/' + workspace_name + '/Frameworks'


if os.path.exists(build_path):
    
    rmCmd = 'rm -rf %s' % build_path
    os.system(rmCmd)


print("当前项目路径------->%s" %(project_path) )
print("当前读取文件路径------->%s" %(podfile_path))
print("工程路径------->%s" %(workspace_name))
print("build路径------->%s" %(build_path))
print("导出路径------->%s" %(product_path))


def readPodfileAllLib(func):
    
    os.system('pod install')
    
    f = open(podfile_path,'r')
    
    lines = f.readlines()
   
    for line in lines:


        patt = re.compile(r'pod(.*)')

        result1 = patt.findall(line)


        # print('11111111111111%s' % result1)

        if len(result1) > 0 and result1[0].find(workspace_name) == -1:

            newline = result1[0]
            result2 = newline.split(',')

            # print('####################%s' % result2)

            if len(result2) > 0:

                newline = result2[0]


                func(newline.replace('\'',''))

    f.close()
            

def transformLibToStaticLib(s):

    s = ''.join(s.split())

    
    print("%s******************开始打包framework🔥 🔥 🔥" % s)

    cleanCmd = 'xcodebuild  clean -workspace %s.xcworkspace ' %(s)
    os.system(cleanCmd)


    os_path = '%s/Os' %(build_path)
    st_path = '%s/St' %(build_path)


    result_library_iphoneos = '%s/Build/Products/Release-iphoneos/%s/%s.framework' %(os_path,s,s)
    result_library_simulator = '%s/Build/Products/Release-iphonesimulator/%s/%s.framework' %(st_path,s,s)
    
    
    pod_library_iphoneos = '%s/%s' %(result_library_iphoneos,s)
    pod_library_simulator = '%s/%s' %(result_library_simulator,s)


    
    result_path = '%s/%s' %(product_path,s)

    if os.path.exists(result_path):
            
            rmCmd = 'rm -rf %s' % result_path
            os.system(rmCmd)


    os.makedirs(result_path) 


    if framkework_Satus == 1:
    
        print('******************打包真机framework🍺 🍺 🍺')
        # 真机
        
        osCmd = 'xcodebuild  build -workspace %s.xcworkspace -scheme %s -configuration Release -derivedDataPath %s -sdk iphoneos' %(workspace_name,s,os_path)
        os.system(osCmd)

        cpCmd = 'cp -rf %s %s' %(result_library_iphoneos,result_path)
        os.system(cpCmd)
        print("%s***************framework真机版本导出成功😃 😃 😃" % s)


    elif framkework_Satus == 2:

        print('******************打包模拟器framework🍺 🍺 🍺')
        # 模拟器
        
        simulatorSmd = 'xcodebuild  build -workspace %s.xcworkspace -scheme %s -configuration Release -derivedDataPath %s -sdk iphonesimulator' %(workspace_name,s,st_path)
        os.system(simulatorSmd)

        cpCmd = 'cp -rf %s %s' %(result_library_simulator,result_path)
        os.system(cpCmd)
        print("%s***************framework模拟器版本导出成功😃 😃 😃" % s)


    else:

        print('******************打包真机framework🍺 🍺 🍺')
        # 真机
        
        osCmd = 'xcodebuild  build -workspace %s.xcworkspace -scheme %s -configuration Release -derivedDataPath %s -sdk iphoneos' %(workspace_name,s,os_path)
        os.system(osCmd)

        print('******************打包模拟器framework🍺 🍺 🍺')
        # 模拟器

        simulatorSmd = 'xcodebuild  build -workspace %s.xcworkspace -scheme %s -configuration Release -derivedDataPath %s -sdk iphonesimulator' %(workspace_name,s,st_path)
        os.system(simulatorSmd)

        lipoCmd = 'lipo -create %s %s -output %s' %(pod_library_iphoneos,pod_library_simulator,pod_library_iphoneos)

        os.system(lipoCmd)
        print("%s***************framework聚合版本导出成功😃 😃 😃" % s)

        cpCmd = 'cp -rf %s %s' %(result_library_iphoneos,result_path)

        os.system(cpCmd)



readPodfileAllLib(transformLibToStaticLib)













