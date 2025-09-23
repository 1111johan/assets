from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import json

class MedicalReportPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """设置自定义样式"""
        # 检查样式是否已存在，避免重复添加
        style_names = [style.name for style in self.styles.byName.values()]
        
        # 标题样式
        if 'CustomTitle' not in style_names:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            ))
        
        # 章节标题样式
        if 'SectionTitle' not in style_names:
            self.styles.add(ParagraphStyle(
                name='SectionTitle',
                parent=self.styles['Heading2'],
                fontSize=14,
                spaceAfter=12,
                spaceBefore=20,
                textColor=colors.darkblue,
                borderWidth=1,
                borderColor=colors.lightblue,
                borderPadding=5
            ))
        
        # 子标题样式
        if 'SubSectionTitle' not in style_names:
            self.styles.add(ParagraphStyle(
                name='SubSectionTitle',
                parent=self.styles['Heading3'],
                fontSize=12,
                spaceAfter=8,
                spaceBefore=12,
                textColor=colors.darkgreen
            ))
        
        # 正文样式
        if 'CustomBodyText' not in style_names:
            self.styles.add(ParagraphStyle(
                name='CustomBodyText',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=6,
                alignment=TA_JUSTIFY,
                leftIndent=0,
                rightIndent=0
            ))
        
        # 病人信息样式
        if 'PatientInfo' not in style_names:
            self.styles.add(ParagraphStyle(
                name='PatientInfo',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=4,
                leftIndent=20,
                textColor=colors.darkblue
            ))

    def generate_pdf(self, patient_data, report_content, output_path):
        """生成PDF报告"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # 添加标题
        title = Paragraph("术前病情预测 & 中西医结合诊疗报告", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # 添加生成时间
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        time_para = Paragraph(f"报告生成时间：{current_time}", self.styles['CustomBodyText'])
        story.append(time_para)
        story.append(Spacer(1, 20))
        
        # 添加病人基本信息
        story.append(Paragraph("一、病人基本信息", self.styles['SectionTitle']))
        
        # 创建病人信息表格
        patient_info_data = [
            ['姓名', patient_data.get('name', '')],
            ['年龄', f"{patient_data.get('age', '')}岁"],
            ['性别', patient_data.get('sex', '')],
            ['主诉', patient_data.get('chief_complaint', '')],
            ['既往病史', patient_data.get('history', '无')],
            ['影像学检查', patient_data.get('imaging', '无')],
            ['其他备注', patient_data.get('additional_notes', '无')]
        ]
        
        patient_table = Table(patient_info_data, colWidths=[1.5*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # 添加实验室检查结果
        if patient_data.get('labs'):
            story.append(Paragraph("二、实验室检查结果", self.styles['SectionTitle']))
            
            labs_data = [['检查项目', '结果', '参考范围']]
            for key, value in patient_data['labs'].items():
                # 根据检查项目添加参考范围
                ref_range = self.get_reference_range(key)
                labs_data.append([key, str(value), ref_range])
            
            labs_table = Table(labs_data, colWidths=[1.5*inch, 1*inch, 2*inch])
            labs_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(labs_table)
            story.append(Spacer(1, 20))
        
        # 添加诊疗报告内容
        story.append(Paragraph("三、诊疗报告", self.styles['SectionTitle']))
        
        # 解析报告内容并格式化
        formatted_report = self.format_report_content(report_content)
        for section in formatted_report:
            story.append(section)
        
        # 添加免责声明
        story.append(Spacer(1, 30))
        disclaimer = Paragraph(
            "<b>免责声明：</b>本报告由AI系统生成，仅供参考，不能替代专业医生的诊断和治疗建议。"
            "请以专业医生的诊断为准，如有疑问请及时就医。",
            self.styles['CustomBodyText']
        )
        story.append(disclaimer)
        
        # 构建PDF
        doc.build(story)
    
    def get_reference_range(self, test_name):
        """获取检查项目的参考范围"""
        reference_ranges = {
            'ALT': '5-40 U/L',
            'AST': '8-40 U/L',
            'ALP': '40-150 U/L',
            '总胆红素': '3.4-20.5 μmol/L',
            '直接胆红素': '0-6.8 μmol/L',
            '白蛋白': '35-55 g/L',
            'AFP': '<20 ng/mL',
            'CA19-9': '<37 U/mL',
            'CEA': '<5 ng/mL'
        }
        return reference_ranges.get(test_name, '请参考实验室标准')
    
    def format_report_content(self, report_content):
        """格式化报告内容"""
        sections = []
        lines = report_content.split('\n')
        
        current_section = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测章节标题
            if line.startswith('##') or line.startswith('**') and '**' in line:
                if current_section:
                    sections.append(Paragraph('\n'.join(current_section), self.styles['CustomBodyText']))
                    current_section = []
                
                # 清理标题格式
                title_text = line.replace('##', '').replace('**', '').strip()
                if title_text:
                    sections.append(Paragraph(title_text, self.styles['SubSectionTitle']))
            
            # 检测子标题
            elif line.startswith('###') or (line.startswith('-') and ':' in line):
                if current_section:
                    sections.append(Paragraph('\n'.join(current_section), self.styles['CustomBodyText']))
                    current_section = []
                
                title_text = line.replace('###', '').replace('-', '').strip()
                if title_text:
                    sections.append(Paragraph(f"• {title_text}", self.styles['CustomBodyText']))
            
            else:
                current_section.append(line)
        
        # 添加最后一部分
        if current_section:
            sections.append(Paragraph('\n'.join(current_section), self.styles['CustomBodyText']))
        
        return sections

def generate_medical_report_pdf(patient_data, report_content, output_path):
    """生成医疗报告PDF的便捷函数"""
    generator = MedicalReportPDFGenerator()
    generator.generate_pdf(patient_data, report_content, output_path)
    return output_path
