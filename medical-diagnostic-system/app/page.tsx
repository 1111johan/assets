"use client"

import { useState } from "react"
import { MedicalSidebar } from "@/components/medical-sidebar"
import { MedicalHeader } from "@/components/medical-header"
import { ModelTrainingSection } from "@/components/model-training-section"
import { EvidencePackageSection } from "@/components/evidence-package-section"
import { PatientReportSection } from "@/components/patient-report-section"
import { AiAssistantSection } from "@/components/ai-assistant-section"
import { ReportOptimizationSection } from "@/components/report-optimization-section"
import { ResearchAnalysisSection } from "@/components/research-analysis-section"
import { HistoryRecordsSection } from "@/components/history-records-section"
import { PatientDetailSection } from "@/components/patient-detail-section"
import { SymptomAnalysisSection } from "@/components/symptom-analysis-section"

export default function MedicalDiagnosticSystem() {
  const [activeSection, setActiveSection] = useState("model-training")
  const [isDarkMode, setIsDarkMode] = useState(false)

  const renderActiveSection = () => {
    switch (activeSection) {
      case "model-training":
        return <ModelTrainingSection />
      case "evidence-package":
        return <EvidencePackageSection />
      case "new-patient":
        return <PatientReportSection />
      case "ai-assistant":
        return <AiAssistantSection />
      case "report-optimization":
        return <ReportOptimizationSection />
      case "research-analysis":
        return <ResearchAnalysisSection />
      case "history":
        return <HistoryRecordsSection />
      case "patient-detail":
        return <PatientDetailSection />
      case "symptom-analysis":
        return <SymptomAnalysisSection />
      default:
        return <ModelTrainingSection />
    }
  }

  return (
    <div className={`flex h-screen bg-background ${isDarkMode ? "dark" : ""}`}>
      <MedicalSidebar activeSection={activeSection} onSectionChange={setActiveSection} />

      <div className="flex-1 flex flex-col min-w-0">
        <MedicalHeader isDarkMode={isDarkMode} onThemeToggle={() => setIsDarkMode(!isDarkMode)} />
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto">{renderActiveSection()}</div>
        </main>
      </div>
    </div>
  )
}
