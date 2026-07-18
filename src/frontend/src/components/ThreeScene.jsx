import React, { useRef, useState, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Points, PointMaterial, Center } from '@react-three/drei'
import * as random from 'maath/random/dist/maath-random.esm'

export function ParticlesBg() {
  const ref = useRef()
  const [sphere] = useState(() => random.inSphere(new Float32Array(3000), { radius: 1.8 }))
  
  useFrame((state, delta) => {
    if (ref.current) {
      ref.current.rotation.x -= delta / 10
      ref.current.rotation.y -= delta / 15
    }
  })

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={sphere} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          color="#818cf8"
          size={0.015}
          sizeAttenuation={true}
          depthWrite={false}
        />
      </Points>
    </group>
  )
}

function DataNode({ position, color, label, size = 0.15 }) {
  const meshRef = useRef()
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = Math.sin(state.clock.getElapsedTime() + position[0]) * 0.2
      meshRef.current.rotation.y = Math.cos(state.clock.getElapsedTime() + position[1]) * 0.2
      meshRef.current.position.y = position[1] + Math.sin(state.clock.getElapsedTime() * 2 + position[0]) * 0.05
    }
  })

  return (
    <mesh ref={meshRef} position={position}>
      <octahedronGeometry args={[size]} />
      <meshStandardMaterial
        color={color}
        wireframe={false}
        roughness={0.1}
        metalness={0.9}
        emissive={color}
        emissiveIntensity={0.5}
      />
    </mesh>
  )
}

function GridLines() {
  return (
    <gridHelper args={[10, 10, '#312e81', '#1e1b4b']} position={[0, -1, 0]} />
  )
}

export function QuantumCore() {
  const groupRef = useRef()
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.getElapsedTime() * 0.15
    }
  })

  // Nodes for the medallion layers
  const nodes = [
    { position: [-1.2, 0.5, 0], color: '#f43f5e', label: 'Bronze' },
    { position: [0, 0.5, 0], color: '#14b8a6', label: 'Silver' },
    { position: [1.2, 0.5, 0], color: '#6366f1', label: 'Gold' },
  ]

  return (
    <group ref={groupRef}>
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={1.5} color="#818cf8" />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#14b8a6" />
      
      {/* Central Quantum Orb */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshPhysicalMaterial
          color="#312e81"
          roughness={0}
          metalness={0.1}
          transmission={0.9}
          thickness={0.5}
          ior={1.5}
          clearcoat={1.0}
        />
      </mesh>
      
      {/* Floating data pipeline stages */}
      {nodes.map((node, i) => (
        <DataNode key={i} position={node.position} color={node.color} label={node.label} />
      ))}

      {/* Outer spinning ring */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[1.5, 0.02, 16, 100]} />
        <meshBasicMaterial color="#4f46e5" transparent opacity={0.3} />
      </mesh>
      
      <GridLines />
    </group>
  )
}
