#!/usr/bin/env node

/**
 * Vercel部署检查脚本
 * 检查项目是否准备好部署到Vercel
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 检查Vercel部署准备情况...\n');

// 检查必需文件
const requiredFiles = [
  'vercel.json',
  'frontend/package.json',
  'frontend/next.config.js',
  'frontend/tsconfig.json',
  'frontend/tailwind.config.js',
  'api/generate_report.py',
  'api/chat.py',
  'api/__init__.py',
  'api/requirements.txt'
];

let allFilesExist = true;

console.log('📁 检查必需文件:');
requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`  ✅ ${file}`);
  } else {
    console.log(`  ❌ ${file} - 文件缺失`);
    allFilesExist = false;
  }
});

// 检查package.json
console.log('\n📦 检查前端依赖:');
try {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'frontend/package.json'), 'utf8'));
  const requiredDeps = ['next', 'react', 'react-dom', 'typescript', 'tailwindcss'];
  
  requiredDeps.forEach(dep => {
    if (packageJson.dependencies[dep] || packageJson.devDependencies[dep]) {
      console.log(`  ✅ ${dep}`);
    } else {
      console.log(`  ❌ ${dep} - 依赖缺失`);
      allFilesExist = false;
    }
  });
} catch (error) {
  console.log('  ❌ package.json 解析失败');
  allFilesExist = false;
}

// 检查vercel.json配置
console.log('\n⚙️ 检查Vercel配置:');
try {
  const vercelConfig = JSON.parse(fs.readFileSync(path.join(__dirname, 'vercel.json'), 'utf8'));
  
  if (vercelConfig.builds && vercelConfig.builds.length > 0) {
    console.log('  ✅ builds 配置正确');
  } else {
    console.log('  ❌ builds 配置缺失');
    allFilesExist = false;
  }
  
  if (vercelConfig.routes && vercelConfig.routes.length > 0) {
    console.log('  ✅ routes 配置正确');
  } else {
    console.log('  ❌ routes 配置缺失');
    allFilesExist = false;
  }
  
  if (vercelConfig.functions) {
    console.log('  ✅ functions 配置正确');
  } else {
    console.log('  ❌ functions 配置缺失');
    allFilesExist = false;
  }
} catch (error) {
  console.log('  ❌ vercel.json 解析失败');
  allFilesExist = false;
}

// 检查环境变量配置
console.log('\n🔐 检查环境变量配置:');
const envExamplePath = path.join(__dirname, 'frontend/env.example');
if (fs.existsSync(envExamplePath)) {
  console.log('  ✅ env.example 文件存在');
} else {
  console.log('  ❌ env.example 文件缺失');
  allFilesExist = false;
}

// 总结
console.log('\n📊 检查结果:');
if (allFilesExist) {
  console.log('🎉 项目已准备好部署到Vercel！');
  console.log('\n📋 部署步骤:');
  console.log('1. 安装Vercel CLI: npm install -g vercel');
  console.log('2. 登录Vercel: vercel login');
  console.log('3. 部署项目: vercel');
  console.log('4. 配置环境变量: 在Vercel Dashboard中设置API密钥');
  console.log('5. 生产部署: vercel --prod');
} else {
  console.log('❌ 项目尚未准备好部署，请修复上述问题');
}

console.log('\n📚 更多信息请查看 VERCEL_DEPLOYMENT_GUIDE.md');
