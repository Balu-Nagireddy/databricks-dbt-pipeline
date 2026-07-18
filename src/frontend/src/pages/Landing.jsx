import React, { useEffect, useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import { motion, useScroll, useTransform, useSpring } from 'framer-motion'
import { ArrowRight, Database, Shield, Zap, RefreshCw, BarChart2, Star, Cpu } from 'lucide-react'
import { useKPIs } from '../hooks/useData'
import { ParticlesBg, QuantumCore } from '../components/ThreeScene'
import { fmtCurrency, fmt } from '../utils/format'

export default function LandingPage({ onEnter }) {
  const containerRef = useRef(null)
  const { data: kpis } = useKPIs()

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end end'],
  })

  const coreScale = useSpring(useTransform(scrollYProgress, [0, 0.5], [1.2, 0.8]), {
    stiffness: 100,
    damping: 30,
  })

  const coreOpacity = useTransform(scrollYProgress, [0, 0.8, 1], [1, 1, 0])

  const steps = [
    { name: 'KaggleHub Ingestion', desc: 'Secure data extraction from cloud repositories.', icon: <Database /> },
    { name: 'Bronze Ingestion', desc: 'Preserves raw structure in compressed Parquet.', icon: <Cpu /> },
    { name: 'Silver Standardization', desc: 'Data quality checks & referential integrity validation.', icon: <Shield /> },
    { name: 'Gold Analytics Marts', desc: 'Aggregates structured into optimized business marts.', icon: <Zap /> },
  ]

  return (
    <div ref={containerRef} className="landing-container">
      {/* 3D background canvas */}
      <div className="landing-3d-bg">
        <Canvas camera={{ position: [0, 0, 3], fov: 60 }}>
          <ParticlesBg />
          <motion.group scale={coreScale} opacity={coreOpacity}>
            <QuantumCore />
          </motion.group>
        </Canvas>
      </div>

      {/* Hero Section */}
      <section className="landing-hero">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="hero-content"
        >
          <div className="badge-glow">Prism Analytics Enterprise</div>
          <h1 className="hero-title">
            Enterprise <span className="gradient-text">Data Pipeline</span> & Analytics Core
          </h1>
          <p className="hero-subtitle">
            A production-ready data engineering platform leveraging Apache Spark, dbt-core, and FastAPI to ingest, model, and serve live business intelligence.
          </p>
          <div className="hero-buttons">
            <button className="btn-primary" onClick={onEnter}>
              Launch Dashboard <ArrowRight size={16} />
            </button>
          </div>
        </motion.div>
      </section>

      {/* Scroll Story Architecture */}
      <section className="landing-section">
        <div className="section-content">
          <h2 className="section-title">The Medallion Pipeline Architecture</h2>
          <div className="pipeline-steps">
            {steps.map((step, idx) => (
              <motion.div
                key={idx}
                className="step-card"
                whileHover={{ scale: 1.05, borderColor: 'var(--indigo-l)' }}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
              >
                <div className="step-icon">{step.icon}</div>
                <h3>{step.name}</h3>
                <p>{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Live Metrics Statistics */}
      <section className="landing-section metrics-section">
        <div className="section-content">
          <h2 className="section-title">Live System Status</h2>
          <div className="metrics-grid">
            <div className="metric-box">
              <span className="metric-value">{fmtCurrency(kpis?.total_revenue || 15843553.24)}</span>
              <span className="metric-label">Total Revenue Processed</span>
            </div>
            <div className="metric-box">
              <span className="metric-value">{fmt(kpis?.total_orders || 99441)}</span>
              <span className="metric-label">Total Validated Orders</span>
            </div>
            <div className="metric-box">
              <span className="metric-value">16</span>
              <span className="metric-label">REST API Endpoints</span>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Footer */}
      <footer className="landing-cta">
        <div className="cta-content">
          <h2>Ready to explore?</h2>
          <button className="btn-large" onClick={onEnter}>
            Enter Platform Core <ArrowRight size={20} />
          </button>
        </div>
      </footer>
    </div>
  )
}
