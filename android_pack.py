#coding:utf-8
#android 打包脚本，window python2.7
import sys 
import os
import subprocess
import time 
import zipfile
import shutil
import stat


#工程目录
workSpace = "D:/workspace/git/android_workspace/AndroidPackCi"
#打包apk前缀名称  如coffee(前缀)_inner(渠道暗码)_1.2.2(版本号).apk 
apkPrefix = 'demo'
#项目版本号
version = '1.0.0'
#微信资源混淆打包用到
zipalignFile = 'D:/soft/develope/andriod/sdk/sdk/build-tools/23.0.2/zipalign'


#监听进程 
def func_listen_process(Process,listener):
	if listener == None or not isinstance(listener,ProcessListener):
		print 'func_listen_process: ' + process + ' listener is null or not processListener interface'
		return
	
	listener.start()
	
	while (True):   
		time.sleep(1)  
		retCode = subprocess.Popen.poll(pro)   
		if retCode is not None:
			listener.end()
			break
		else:
			listener.doing()
			
		
		
			

#文件重命名
def func_renameFile(path,oldName,newName):
	os.rename(path + '/' + oldName,path + '/' + newName)
	
#删除path 路径下，除extra列表之外的文件
def func_delFiles(path , extra):
	if os.path.exists(path):

		files = os.listdir(path)
		for f in files :
			if os.path.isfile(path + '/'+f) and f not in extra:
				os.remove(path + '/'+f)



#多渠道打正式包
def func_channelsReleasePack(workSpace):
	apkPath = workSpace + '/app/build/outputs/apk'
	channelsFile = open(workSpace + '/channelsFile.txt', "r")
	apks = []

	countApk = 0
	global version
	
	
	print u"\nstart channle release pack\n"
	
	while True:  
		channelName = channelsFile.readline() 
		channelName = channelName.strip('\n').strip('\t')
								
		if channelName:
			channelApkName = apkPath + '/' + apkPrefix + '_' + channelName + '_' + version +'.apk'
			shutil.copyfile(apkPath+'/' + apkPrefix + '_inner_' + ''+ version +'.apk',channelApkName)
			apks.append(apkPrefix + '_' + channelName + '_' + version +'.apk')
			zipped = zipfile.ZipFile(channelApkName, 'a', zipfile.ZIP_DEFLATED)					
			empty_channel_file = "META-INF/channel_{channel}".format(channel = channelName)
			newChannelFile = open(apkPath+'/channel_'+ channelName, 'w')
			newChannelFile.close()
			zipped.write(apkPath+'/channel_'+ channelName,empty_channel_file)
			zipped.close();
			os.remove(apkPath+'/channel_'+ channelName)
			print '---> /' + apkPrefix +'_' + channelName + '_' + version +'.apk'
			
			countApk = countApk + 1;
			
		else:
			channelsFile.close()
			#删除出多余的文件
			func_delFiles(apkPath,apks)
			break
	print u"\nend channle release pack"
	return countApk;
	
def func_andResGuard(apkPath,isChannels = False):
	guardJarFile = workSpace + '/AndResGuard/AndResGuard-cli-1.1.0.jar'
	guardConfigFile = workSpace + '/AndResGuard/config.xml'

	outDir = workSpace + '/AndResGuard/build'
	cmd = 'java -jar ' + guardJarFile  + ' '+apkPath + ' -config ' + guardConfigFile + ' -out '+ outDir +' -zipalign ' + zipalignFile
	proc = subprocess.Popen(cmd,shell = True)
	if isChannels:
		func_listen_process(proc,AndResGuardProcessListener(apkPath,True))
	else:
		func_listen_process(proc,AndResGuardProcessListener(apkPath))
	
#抽象类加抽象方法就等于面向对象编程中的接口  
from abc import ABCMeta,abstractmethod 
#定义接口
class ProcessListener:
	__metaclass__ = ABCMeta #指定这是一个抽象类
	@abstractmethod  #抽象方法
	def start(self):
		pass
	@abstractmethod  #抽象方法
	def doing(self):
		pass
	@abstractmethod  #抽象方法
	def end(self):
		pass

#gradle打包进程监听器		
class GradlePackProcessListener(ProcessListener):
	curTime = 0
	apkCount = 0
	
	def __init__(self):
		return
	def start(self):
		self.curTime = time.time()
	def doing(self):
		return
	def end(self):
		if type == 0:#inner release版
			print u"\nstart channle release pack\n"
			apkName =  apkPrefix + '_inner_' + version + '.apk'

			func_delFiles(workSpace + '/app/build/outputs/apk',[apkName])
			print u"\nend channle debug pack"
			print '---> /' + apkPrefix +'_' + 'inner' + '_' + version +'.apk'
			self.curTime = time.time() - self.curTime;
			print "\nandroid channels pack cost total time :	" + str(int(self.curTime)) +'s , ' + str(1) + ' apks'
		
		#所有渠道release版 
		elif type == 1:
			apkCount = func_channelsReleasePack(workSpace)
			self.curTime = time.time() - self.curTime;
			print "\nandroid channels pack cost total time :	" + str(int(self.curTime)) +'s , ' + str(apkCount) + ' apks'
		
		
		#inner 资源混淆release版
		elif type == 2:
			print u"\nstart channle release pack\n"
			apkName =  apkPrefix + '_inner_' + version + '.apk'
			#func_renameFile(workSpace + '/build/outputs/apk','Yuanlai_Coffee_AndroidPhone-inner-debug.apk',apkName)
			func_delFiles(workSpace + '/app/build/outputs/apk',[apkName])
			print u"\nend channle debug pack"
			print '---> /' + apkPrefix +'_inner_' + version +'.apk'
			self.curTime = time.time() - self.curTime;
			print "\nandroid channels pack cost total time :	" + str(int(self.curTime)) +'s , ' + str(1) + ' apks'
			
			#资源混淆
			func_andResGuard(workSpace  + '/app/build/outputs/apk/'+apkName)
			
		#所有渠道资源混淆release版
		elif type == 3:
		    #先资源混淆在多渠道打包

			apkName =  apkPrefix + '_inner_' + version + '.apk'
			func_andResGuard(workSpace  + '/app/build/outputs/apk/'+apkName,True)

#andResGuard进程监听器		
class AndResGuardProcessListener(ProcessListener):
	curTime = 0
	isChannels = False
	apkPath = ''
	preApkSize = 0
	
	def __init__(self,apkPath,isChannels = False):
		self.isChannels = isChannels
		self.apkPath = apkPath
	def start(self):
		size =os.path.getsize(self.apkPath)
		self.preApkSize = size /float(1024)/1024
	
		self.curTime = time.time()
		print '\n ------>  AndResGuard start \n'	
	def doing(self):
		return
	def end(self):
		time.sleep(30)
		files = os.listdir(workSpace + '/AndResGuard/build')
		for f in files :
			if 'signed_7zip_aligned' in f:
				size = os.path.getsize(workSpace + '/AndResGuard/build/' + f)
				print '\n ------>  AndResGuard before apk size : ' + str(float('%0.2f'%(self.preApkSize))) + 'M\n'
				size = size /float(1024)/1024
				print '\n ------>  AndResGuard after apk size : ' + str(float('%0.2f'%size)) + 'M\n'
				os.chmod( self.apkPath, stat.S_IWRITE )
				os.remove(self.apkPath)
				shutil.copyfile(workSpace + '/AndResGuard/build/' + f,self.apkPath)
				break
		else :
			print ''
		self.curTime = time.time() - self.curTime - 10
		print '\n ------>  AndResGuard end , cost time '+ str(int(self.curTime)) +'s\n\n'
		
		if self.isChannels:
			func_channelsReleasePack(workSpace)
		
		

reload(sys) 
sys.setdefaultencoding('utf8')
print u"\n  请输入数字\n"
hint = u"  0:inner release版   \
           \n  1:所有渠道release版    \
           \n  2:inner 资源混淆release版 \
		   \n  3:所有渠道资源混淆release版\n"
print hint

#type = -1;

while(True):
	type = raw_input("  type = ")
	try:
		type = int(type)
		if type >= 0 and type <= 3:
			break;
		else:
			print u"  \n请输入0-3之间的整数！\n"
	except Exception,e:
		print u"  \n请输入0-3之间的整数！\n"

		
#进入工程目录
os.chdir(workSpace)

cmd = 'gradle assembleInnerRelease '


pro = subprocess.Popen(cmd,shell = True)

#监听gradle 打包进程
func_listen_process(pro,GradlePackProcessListener())




	
