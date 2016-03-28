# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in D:\soft\develope\andriod\sdk\sdk/tools/proguard/proguard-android.txt
# You can edit the include path and order by changing the proguardFiles
# directive in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Add any project specific keep options here:

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# support-v4
-dontwarn android.support.v4.**
-keep class android.support.v4.app.** { *; }
-keep interface android.support.v4.app.** { *; }
# support-v4

# support-v7
-dontwarn android.support.v7.**
-keep class android.support.v7.widget.Toolbar { *; } #解决反射问题
-keep class android.support.v7.internal.** { *; }
-keep interface android.support.v7.internal.** { *; }
# support-v7

# android.support.design
-keep class android.support.design.** {*;}
# android.support.design

