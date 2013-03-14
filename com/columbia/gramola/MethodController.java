package com.columbia.gramola;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;

import javax.tools.JavaCompiler;
import javax.tools.ToolProvider;

public class MethodController {
	
	private static String rootPath = "/Users/mikefhsu/course/PLT/Javatest";
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String fileName = "FirstAttempt";
		String targetPath = creatJavaFile(fileName, "String", null, null);
		int result = compileJavaFile(targetPath);
		
		if (result == 0) {
			System.out.println("Compilation of " + targetPath + " succeeds");
		} else {
			System.out.println("Compilation error: " + result);
		}
		
		executeClass(fileName);
	}
	
	public static String creatJavaFile(String className, String returnType,
			String param, String contents) {
		StringBuilder sBuilder = new StringBuilder();
		sBuilder.append("public class " + className + "{\n");
		sBuilder.append("	public " + returnType + " " + "run " + "()"  + "{\n");
		sBuilder.append("		return \"" + className + "\";\n");
		sBuilder.append("	}\n");
		sBuilder.append("}\n");
		System.out.println(sBuilder.toString());
		
		String target = rootPath + "/" + className + ".java";
		FileWriter fw;
		try {
			File tmpFile = new File(target);
			if (tmpFile.exists()) {
				tmpFile.delete();
			}
			
			fw = new FileWriter(target, true);
			fw.write(sBuilder.toString());
			fw.close();
			
			System.out.println(className + ".java has been created");
			
			return target;
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		return null;
	}
	
	public static int compileJavaFile(String target) {
		JavaCompiler jc = ToolProvider.getSystemJavaCompiler();
		int result = jc.run(null, null, null, target);
		
		return result;
	}
	
	public static void executeClass(String target) {
		File root = new File(rootPath);
		
		if (!root.exists()) {
			System.out.println("The root folder " + target + " does not exist");
		} else if (!root.isDirectory()) {
			System.out.println("The root folder " + target + " is not a directory");
		}
	
		try {
			System.out.println("Test target: " + target);
			URLClassLoader cLoader = URLClassLoader.
					newInstance(new URL[]{root.toURI().toURL()});
			
			Class<?> targetClass = Class.forName(target, false, cLoader);
			Object targetInstance = targetClass.newInstance();
			Method targetMethod = targetClass.getMethod("run", null);
			String returnVal = (String)targetMethod.invoke(targetInstance);
			System.out.println("Test return value: " + returnVal);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
