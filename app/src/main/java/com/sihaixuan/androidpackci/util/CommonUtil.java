package com.sihaixuan.androidpackci.util;

import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.util.Log;

import java.io.IOException;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 * Created by toney on 2016/3/28.
 */
public class CommonUtil {
    private final static String TAG = "CommonUtil";
    private CommonUtil(){}


    /**
     * 获取友盟渠道
     * #app安装后，拷贝保存在/data/app/目录下
     * @return
     */
    public static String getChannelByFileName(Context context) {

        String sourceDir = context.getApplicationInfo().sourceDir;
        String ret = "";
        ZipFile zipfile = null;
        try {
            Log.d(TAG, "app source dir : " + sourceDir);
            zipfile = new ZipFile(sourceDir);
            Enumeration<?> entries = zipfile.entries();
            while (entries.hasMoreElements()) {
                ZipEntry entry = ((ZipEntry) entries.nextElement());
                String entryName = entry.getName();
                Log.d(TAG,entryName + "");
                if (entryName.contains("channel")) {
                    ret = entryName;
                    break;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (zipfile != null) {
                try {
                    zipfile.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        String[] split = ret.split("_");
        if (split != null && split.length >= 2) {
            return ret.substring(split[0].length() + 1);

        } else {
            return "";
        }
    }
}
