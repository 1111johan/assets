'use client'

import { useState } from 'react'
import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { NewPatientForm } from '@/components/NewPatientForm'
import { HistoryPage } from '@/components/HistoryPage'
import { AIChatPage } from '@/components/AIChatPage'
import { ReportOptimizePage } from '@/components/ReportOptimizePage'
import { SymptomAnalysisPage } from '@/components/SymptomAnalysisPage'
import { ResearchDataPage } from '@/components/ResearchDataPage'
import { ModelTrainingPage } from '@/components/ModelTrainingPage'
import { EvidenceBundlePage } from '@/components/EvidenceBundlePage'
import { SettingsPage } from '@/components/SettingsPage'

type PageType = 
  | 'new-patient' 
  | 'history' 
  | 'ai-chat' 
  | 'report-optimize' 
  | 'symptom-analysis' 
  | 'research-data' 
  | 'model-training' 
  | 'evidence-bundle' 
  | 'settings'

export default function Home() {
  const [currentPage, setCurrentPage] = useState<PageType>('new-patient')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const renderPage = () => {
    switch (currentPage) {
      case 'new-patient':
        return <NewPatientForm />
      case 'history':
        return <HistoryPage />
      case 'ai-chat':
        return <AIChatPage />
      case 'report-optimize':
        return <ReportOptimizePage />
      case 'symptom-analysis':
        return <SymptomAnalysisPage />
      case 'research-data':
        return <ResearchDataPage />
      case 'model-training':
        return <ModelTrainingPage />
      case 'evidence-bundle':
        return <EvidenceBundlePage />
      case 'settings':
        return <SettingsPage />
      default:
        return <NewPatientForm />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="flex">
        <Sidebar 
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />
        
        <main className="flex-1 p-6">
          {renderPage()}
        </main>
      </div>
    </div>
  )
}
