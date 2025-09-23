"use client"

import { useState } from "react"
import {
  ChevronDown,
  Target,
  Rocket,
  BarChart3,
  Settings,
  CheckCircle,
  Clock,
  Activity,
  Zap,
  TrendingUp,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function ModelTrainingSection() {
  const [modelType, setModelType] = useState("诊断分类模型")
  const [algorithm, setAlgorithm] = useState("xgboost")
  const [isTraining, setIsTraining] = useState(false)
  const [trainingProgress, setTrainingProgress] = useState(0)
  const [trainingStatus, setTrainingStatus] = useState<"idle" | "training" | "completed">("idle")

  const [advancedParams, setAdvancedParams] = useState({
    testSize: 0.2,
    randomState: 42,
    crossValidation: 5,
    maxDepth: 6,
    learningRate: 0.1,
    nEstimators: 100,
  })

  const handleStartTraining = () => {
    setIsTraining(true)
    setTrainingStatus("training")
    setTrainingProgress(0)

    // Simulate training progress
    const interval = setInterval(() => {
      setTrainingProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsTraining(false)
          setTrainingStatus("completed")
          return 100
        }
        return prev + Math.random() * 15
      })
    }, 500)
  }

  return (
    <div className="p-8 space-y-8 animate-fade-in-up">
      {/* Model Training Header */}
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-green-500/20 to-green-600/20 border border-green-500/30 rounded-xl">
            <Activity className="h-6 w-6 text-green-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-foreground">模型训练</h2>
            <p className="text-muted-foreground mt-1">训练诊断、生存分析、复发预测等机器学习模型</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="medical-metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">活跃模型</p>
                <p className="text-2xl font-bold text-foreground">3</p>
              </div>
              <Target className="h-8 w-8 text-primary/60" />
            </div>
          </div>
          <div className="medical-metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">训练完成</p>
                <p className="text-2xl font-bold text-foreground">12</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-400/60" />
            </div>
          </div>
          <div className="medical-metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">平均准确率</p>
                <p className="text-2xl font-bold text-foreground">94.2%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-400/60" />
            </div>
          </div>
        </div>
      </div>

      {/* Model Configuration */}
      <Card className="dashboard-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <Settings className="h-5 w-5 text-primary" />
            模型配置
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-3">
            <label className="text-sm font-medium text-foreground">选择模型类别</label>
            <div className="relative">
              <select
                value={modelType}
                onChange={(e) => setModelType(e.target.value)}
                className="medical-input-modern w-full appearance-none pr-12"
              >
                <option value="诊断分类模型">诊断分类模型</option>
                <option value="预后预测模型">预后预测模型</option>
                <option value="风险评估模型">风险评估模型</option>
                <option value="生存分析模型">生存分析模型</option>
                <option value="复发预测模型">复发预测模型</option>
              </select>
              <ChevronDown className="absolute right-4 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Diagnostic Classification Model Training */}
      <Card className="dashboard-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-3">
            <Target className="h-5 w-5 text-red-400" />
            诊断分类模型训练
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <label className="text-sm font-medium text-foreground">数据文件路径</label>
              <input
                type="text"
                value="research_data/sample_medical_data.csv"
                readOnly
                className="medical-input-modern text-muted-foreground cursor-not-allowed"
              />
            </div>

            <div className="space-y-3">
              <label className="text-sm font-medium text-foreground">模型算法</label>
              <div className="relative">
                <select
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value)}
                  className="medical-input-modern w-full appearance-none pr-12"
                >
                  <option value="xgboost">XGBoost</option>
                  <option value="random_forest">Random Forest</option>
                  <option value="svm">Support Vector Machine</option>
                  <option value="neural_network">Neural Network</option>
                  <option value="logistic_regression">Logistic Regression</option>
                  <option value="gradient_boosting">Gradient Boosting</option>
                </select>
                <ChevronDown className="absolute right-4 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <label className="text-sm font-medium text-foreground">目标变量列名</label>
            <input
              type="text"
              value="diagnosis_target"
              readOnly
              className="medical-input-modern text-muted-foreground cursor-not-allowed"
            />
          </div>

          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-base">
                <Zap className="h-4 w-4 text-yellow-400" />
                高级参数配置
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    测试集比例
                  </label>
                  <input
                    type="number"
                    value={advancedParams.testSize}
                    onChange={(e) =>
                      setAdvancedParams((prev) => ({ ...prev, testSize: Number.parseFloat(e.target.value) }))
                    }
                    step="0.1"
                    min="0.1"
                    max="0.5"
                    className="w-full p-3 bg-input/30 border border-border/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-200"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    交叉验证折数
                  </label>
                  <input
                    type="number"
                    value={advancedParams.crossValidation}
                    onChange={(e) =>
                      setAdvancedParams((prev) => ({ ...prev, crossValidation: Number.parseInt(e.target.value) }))
                    }
                    min="3"
                    max="10"
                    className="w-full p-3 bg-input/30 border border-border/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-200"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">随机种子</label>
                  <input
                    type="number"
                    value={advancedParams.randomState}
                    onChange={(e) =>
                      setAdvancedParams((prev) => ({ ...prev, randomState: Number.parseInt(e.target.value) }))
                    }
                    className="w-full p-3 bg-input/30 border border-border/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-200"
                  />
                </div>
                {algorithm === "xgboost" && (
                  <>
                    <div className="space-y-2">
                      <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                        最大深度
                      </label>
                      <input
                        type="number"
                        value={advancedParams.maxDepth}
                        onChange={(e) =>
                          setAdvancedParams((prev) => ({ ...prev, maxDepth: Number.parseInt(e.target.value) }))
                        }
                        min="3"
                        max="15"
                        className="w-full p-3 bg-input/30 border border-border/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-200"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                        学习率
                      </label>
                      <input
                        type="number"
                        value={advancedParams.learningRate}
                        onChange={(e) =>
                          setAdvancedParams((prev) => ({ ...prev, learningRate: Number.parseFloat(e.target.value) }))
                        }
                        step="0.01"
                        min="0.01"
                        max="1"
                        className="w-full p-3 bg-input/30 border border-border/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-200"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                        估计器数量
                      </label>
                      <input
                        type="number"
                        value={advancedParams.nEstimators}
                        onChange={(e) =>
                          setAdvancedParams((prev) => ({ ...prev, nEstimators: Number.parseInt(e.target.value) }))
                        }
                        min="50"
                        max="1000"
                        step="50"
                        className="w-full p-3 bg-input/30 border border-border/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-200"
                      />
                    </div>
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          {trainingStatus !== "idle" && (
            <Card className="dashboard-card-gradient animate-scale-in">
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-base">
                  {trainingStatus === "training" && <Clock className="h-5 w-5 animate-spin text-blue-400" />}
                  {trainingStatus === "completed" && <CheckCircle className="h-5 w-5 text-green-400" />}
                  训练状态
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-3">
                  <div className="flex justify-between text-sm font-medium">
                    <span>训练进度</span>
                    <span className="text-primary">{Math.round(trainingProgress)}%</span>
                  </div>
                  <Progress value={trainingProgress} className="h-3" />
                </div>
                {trainingStatus === "training" && (
                  <div className="text-sm text-blue-400 font-medium animate-pulse">
                    正在训练 {algorithm} 模型，请稍候...
                  </div>
                )}
                {trainingStatus === "completed" && (
                  <div className="space-y-4">
                    <div className="text-sm text-green-400 font-bold">✨ 训练完成！</div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-green-500/10 border border-green-500/20 p-4 rounded-lg">
                        <div className="text-xs text-green-400 font-medium uppercase tracking-wider">准确率</div>
                        <div className="text-xl font-bold text-green-400">94.2%</div>
                      </div>
                      <div className="bg-blue-500/10 border border-blue-500/20 p-4 rounded-lg">
                        <div className="text-xs text-blue-400 font-medium uppercase tracking-wider">精确率</div>
                        <div className="text-xl font-bold text-blue-400">92.8%</div>
                      </div>
                      <div className="bg-purple-500/10 border border-purple-500/20 p-4 rounded-lg">
                        <div className="text-xs text-purple-400 font-medium uppercase tracking-wider">召回率</div>
                        <div className="text-xl font-bold text-purple-400">91.5%</div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          <div className="pt-6 flex flex-col sm:flex-row gap-4">
            <Button
              onClick={handleStartTraining}
              disabled={isTraining}
              className="medical-button-primary flex items-center gap-3 text-base"
            >
              {isTraining ? (
                <>
                  <Clock className="h-5 w-5 animate-spin" />
                  训练中...
                </>
              ) : (
                <>
                  <Rocket className="h-5 w-5" />
                  开始训练诊断模型
                </>
              )}
            </Button>

            {trainingStatus === "completed" && (
              <Button
                variant="outline"
                className="medical-button-secondary flex items-center gap-3 text-base bg-transparent"
              >
                <BarChart3 className="h-5 w-5" />
                查看训练报告
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
