import React, { useState } from 'react';
import { Download } from 'lucide-react';
import jsPDF from 'jspdf';

const QuickActions = ({ metrics, formData, videoData }) => {
  const [downloadStatus, setDownloadStatus] = useState('');

  const generatePDF = () => {
    // Verificar que tenemos los datos necesarios
    if (!formData || !metrics || !videoData) {
      throw new Error('Missing required data for PDF generation');
    }

    const doc = new jsPDF();
    
    // Calcular métricas ROI con valores por defecto
    const minBrandTime = parseInt(formData.min_brand_time) || 1;
    const totalTime = metrics.total_time_seconds || 0;
    const contractPrice = parseFloat(formData.contract_price) || 0;
    const views = videoData.views || 1;
    const comments = videoData.comments || 1;
    
    const exposicionEfectiva = (totalTime / minBrandTime) * 100;
    const roiPorVisualizacion = contractPrice / views;
    const costePorEngagement = contractPrice / comments;
    const engagementRate = (comments / views) * 100;
    
    // Colores corporativos
    const primaryColor = [44, 62, 80]; 
    const accentColor = [231, 76, 60]; 
    const successColor = [39, 174, 96]; 
    const grayColor = [127, 140, 141]; 
    
    let yPos = 30;
    
    // Header
    doc.setFontSize(24);
    doc.setTextColor(...primaryColor);
    doc.setFont('helvetica', 'bold');
    doc.text('LogoTracker', 20, yPos);
    
    doc.setTextColor(...accentColor);
    doc.text('Pro', 75, yPos);
    
    // Subtítulo
    yPos += 15;
    doc.setFontSize(16);
    doc.setTextColor(...primaryColor);
    doc.setFont('helvetica', 'normal');
    doc.text('ROI Analysis Report', 20, yPos);
    
    // Fecha
    yPos += 10;
    doc.setFontSize(10);
    doc.setTextColor(...grayColor);
    doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 20, yPos);
    
    // Línea separadora
    yPos += 8;
    doc.setDrawColor(...accentColor);
    doc.setLineWidth(1);
    doc.line(20, yPos, 190, yPos);
    
    // Vista general de la campaña
    yPos += 15;
    doc.setFontSize(14);
    doc.setTextColor(...primaryColor);
    doc.setFont('helvetica', 'bold');
    doc.text('Campaign Overview', 20, yPos);
    
    // Background para la sección
    yPos += 5;
    doc.setFillColor(248, 249, 250);
    doc.rect(15, yPos, 180, 35, 'F');
    
    yPos += 12;
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(52, 73, 94);
    
    doc.text(`Brand Analyzed: ${formData.brand || 'N/A'}`, 20, yPos);
    doc.text(`Contract Investment: €${contractPrice}`, 110, yPos);
    
    yPos += 8;
    doc.text(`Total Views: ${views.toLocaleString()}`, 20, yPos);
    doc.text(`Comments: ${comments.toLocaleString()}`, 110, yPos);
    
    yPos += 8;
    doc.text(`Platform: ${videoData.platform || 'YouTube'}`, 20, yPos);
    doc.text(`Influencer: ${videoData.influencer || 'Not available'}`, 110, yPos);
    
    yPos += 8;
    doc.text('Video URL: ', 20, yPos);
    // link clickable
    const videoUrl = videoData.url || 'N/A';
    const maxUrlLength = 60;
    const displayUrl = videoUrl.length > maxUrlLength ? videoUrl.substring(0, maxUrlLength) + '...' : videoUrl;
    doc.setTextColor(0, 0, 255); // azul para link
    doc.textWithLink(displayUrl, 45, yPos, { url: videoUrl });
    
    // SecciÓN DE RESULTADOS DE DETECCIÓN DE LOGOS
    yPos += 20;
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(...primaryColor);
    doc.text('Logo Detection Results', 20, yPos);
    
    yPos += 5;
    doc.setFillColor(248, 249, 250);
    doc.rect(15, yPos, 180, 30, 'F');
    
    yPos += 12;
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(52, 73, 94);
    
    doc.text(`Logo Exposure Time: ${totalTime}s (Required: ${minBrandTime}s)`, 20, yPos);
    
    yPos += 8;
    doc.text(`Average Logo Area: ${metrics.average_area_percentage || 0}% (Required: ${formData.min_logo_area || 0}%)`, 20, yPos);
    
    yPos += 8;
    doc.text(`Detection Confidence: ${metrics.confidence_score || 0}%`, 20, yPos);
    
    yPos += 8;
    const complianceText = `Contract Status: ${metrics.contract_compliant ? 'COMPLIANT' : 'NON-COMPLIANT'}`;
    if (metrics.contract_compliant) {
      doc.setTextColor(...successColor);
    } else {
      doc.setTextColor(...accentColor);
    }
    doc.text(complianceText, 20, yPos);
    
    // Sección de análisis ROI
    yPos += 20;
    doc.setFillColor(241, 242, 246);
    doc.rect(15, yPos - 5, 180, 55, 'F');
    
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(...primaryColor);
    doc.text('ROI Analysis', 20, yPos + 5);
    
    yPos += 20;
    doc.setFontSize(11);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(...accentColor);
    
    // Métricas ROI 
    doc.text(`Exposure Effectiveness: ${Math.min(exposicionEfectiva, 100).toFixed(1)}%`, 20, yPos);
    doc.text(`Cost per View: €${roiPorVisualizacion.toFixed(3)}`, 110, yPos);
    
    yPos += 12;
    doc.text(`Cost per Engagement: €${costePorEngagement.toFixed(2)}`, 20, yPos);
    doc.text(`Engagement Rate: ${engagementRate.toFixed(2)}%`, 110, yPos);
    
    // Recomendaciones estratégicas
    doc.addPage();
    yPos = 30;
    
    // Header para nueva página
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(...primaryColor);
    doc.text('Strategic Recommendations', 20, yPos);
    
    yPos += 15;
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(52, 73, 94);
    
    // Recomendaciones
    let hasRecommendations = false;
    
    if (exposicionEfectiva < 70) {
      hasRecommendations = true;
      doc.setFont('helvetica', 'bold');
      doc.text('Brand Exposure Improvement:', 20, yPos);
      yPos += 8;
      doc.setFont('helvetica', 'normal');
      doc.text('Consider negotiating longer exposure times or more prominent logo', 25, yPos);
      yPos += 6;
      doc.text('placement in future collaborations. Current effectiveness is below', 25, yPos);
      yPos += 6;
      doc.text('optimal levels.', 25, yPos);
      yPos += 15;
    }
    
    if (costePorEngagement > 5) {
      hasRecommendations = true;
      doc.setFont('helvetica', 'bold');
      doc.text('Engagement Optimization:', 20, yPos);
      yPos += 8;
      doc.setFont('helvetica', 'normal');
      doc.text('Focus on influencers with higher engagement rates to improve', 25, yPos);
      yPos += 6;
      doc.text('cost-effectiveness. Current CPE is above industry benchmarks.', 25, yPos);
      yPos += 15;
    }
    
    if (metrics.contract_compliant) {
      hasRecommendations = true;
      doc.setTextColor(...successColor);
      doc.setFont('helvetica', 'bold');
      doc.text('Partnership Success:', 20, yPos);
      yPos += 8;
      doc.setFont('helvetica', 'normal');
      doc.text('This collaboration met all requirements. Consider similar', 25, yPos);
      yPos += 6;
      doc.text('partnerships with this influencer for future campaigns.', 25, yPos);
      yPos += 15;
    } else {
      hasRecommendations = true;
      doc.setTextColor(...accentColor);
      doc.setFont('helvetica', 'bold');
      doc.text('Contract Compliance Issue:', 20, yPos);
      yPos += 8;
      doc.setFont('helvetica', 'normal');
      doc.text('Requirements were not fully met. Review contractual terms', 25, yPos);
      yPos += 6;
      doc.text('and expectations for future collaborations.', 25, yPos);
      yPos += 15;
    }
    
    if (!hasRecommendations) {
      doc.text('All metrics are within acceptable ranges. Continue with', 20, yPos);
      yPos += 6;
      doc.text('current collaboration strategy.', 20, yPos);
    }
    
    // FOOTER 
    const pageHeight = doc.internal.pageSize.height;
    doc.setFontSize(8);
    doc.setTextColor(...grayColor);
    doc.text('LogoTracker Pro | AI-Powered Brand Detection & Analysis', 20, pageHeight - 20);
    
    // URL del video 
    const footerVideoUrl = videoData.url || 'N/A';
    const maxFooterUrlLength = 80;
    const footerDisplayUrl = footerVideoUrl.length > maxFooterUrlLength ? footerVideoUrl.substring(0, maxFooterUrlLength) + '...' : footerVideoUrl;
    doc.text(`Video URL: ${footerDisplayUrl}`, 20, pageHeight - 10);
    
    return doc;
  };

  const handleDownloadReport = async () => {
    setDownloadStatus('generating');
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const doc = generatePDF();
      const fileName = `LogoTracker-ROI-Report-${formData.brand}-${new Date().toISOString().split('T')[0]}.pdf`;
      
      doc.save(fileName);
      
      setDownloadStatus('success');
      setTimeout(() => setDownloadStatus(''), 3000);
      
    } catch (error) {
      console.error('Error generating PDF:', error);
      setDownloadStatus('error');
      setTimeout(() => setDownloadStatus(''), 3000);
    }
  };

  const getDownloadButtonText = () => {
    switch (downloadStatus) {
      case 'generating':
        return 'Generating PDF...';
      case 'success':
        return 'Downloaded!';
      case 'error':
        return 'Try Again';
      default:
        return 'Download ROI Report';
    }
  };

  const getDownloadButtonClass = () => {
    const baseClass = "w-full px-6 py-4 font-semibold transition-all duration-300 font-montserrat rounded-button";
    
    switch (downloadStatus) {
      case 'generating':
        return `${baseClass} bg-petroleo-300 text-white cursor-not-allowed`;
      case 'success':
        return `${baseClass} bg-green-500 text-white`;
      case 'error':
        return `${baseClass} bg-coral-500 text-white hover:bg-coral-600`;
      default:
        return `${baseClass} text-white bg-coral-gradient hover:shadow-coral`;
    }
  };

  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <h3 className="mb-6 text-2xl font-bold font-montserrat text-petroleo-500">
        Actions
      </h3>
      <div className="space-y-4">
        <button 
          onClick={handleDownloadReport}
          disabled={downloadStatus === 'generating'}
          className={getDownloadButtonClass()}
        >
          <div className="flex items-center justify-center space-x-2">
            <Download className={`w-5 h-5 ${downloadStatus === 'generating' ? 'animate-bounce' : ''}`} />
            <span>{getDownloadButtonText()}</span>
          </div>
        </button>
      </div>
    </div>
  );
};

export default QuickActions;