<template>
  <div class="court-3d-container">
    <div class="controls-panel">
      <h3>3D法庭控制面板</h3>
      <div class="control-group">
        <label>控制视角</label>
        <button @click="rotateScene">旋转场景</button>
        <button @click="toggleAnimation">{{ isAnimating ? '停止动画' : '开始动画' }}</button>
      </div>
      <div class="control-group">
        <label>缩放</label>
        <button @click="zoomIn">放大</button>
        <button @click="zoomOut">缩小</button>
      </div>
      <div class="control-group">
        <label>切换视角</label>
        <button @click="viewFront">正面</button>
        <button @click="viewTop">顶部</button>
        <button @click="viewSide">侧面</button>
      </div>
    </div>
    <div :ref="setRendererContainer" class="renderer-container"></div>
  </div>
</template>

<script>
import * as THREE from 'three';
import { markRaw, ref, onMounted, onBeforeUnmount } from 'vue';

export default {
  name: 'CourtRoom3D',
  setup() {
        // 使用ref来引用DOM元素
        const rendererContainer = ref(null);
        // 设置模板引用的回调函数
        const setRendererContainer = (el) => {
          rendererContainer.value = el;
          // 当元素可用时，初始化Three.js
          if (el) {
            initThree();
            createSimpleCourtScene();
            renderScene();
            window.addEventListener('resize', onWindowResize);
          }
        };
      
        // 非响应式变量存储Three.js对象
    let scene = null;
    let camera = null;
    let renderer = null;
    let animationId = null;
    let isAnimating = false;
    let rotationSpeed = 0.01;
    let scaleLevel = 1;
    
    // 初始化Three.js
    const initThree = () => {
      // 创建场景并使用markRaw避免响应式转换
      scene = markRaw(new THREE.Scene());
      scene.background = new THREE.Color(0x1a1a2e);
      
      // 创建相机并使用markRaw
      camera = markRaw(new THREE.PerspectiveCamera(
        75,
        rendererContainer.value.clientWidth / rendererContainer.value.clientHeight,
        0.1,
        1000
      ));
      camera.position.set(0, 10, 30);
      camera.lookAt(0, 0, 0);
      
      // 创建渲染器并使用markRaw
      renderer = markRaw(new THREE.WebGLRenderer({ antialias: true }));
      renderer.setSize(rendererContainer.value.clientWidth, rendererContainer.value.clientHeight);
      rendererContainer.value.appendChild(renderer.domElement);
      
      // 添加简单的环境光
      const ambientLight = markRaw(new THREE.AmbientLight(0xffffff, 0.6));
      scene.add(ambientLight);
      
      // 添加方向光
      const directionalLight = markRaw(new THREE.DirectionalLight(0xffffff, 0.8));
      directionalLight.position.set(10, 20, 15);
      scene.add(directionalLight);
    };
    
    // 创建简单的法庭场景
    const createSimpleCourtScene = () => {
      // 使用基础材质
      const floorMaterial = markRaw(new THREE.MeshBasicMaterial({ color: 0x808080 }));
      const wallMaterial = markRaw(new THREE.MeshBasicMaterial({ color: 0x4a5568 }));
      const judgeMaterial = markRaw(new THREE.MeshBasicMaterial({ color: 0x8b4513 }));
      const plaintiffMaterial = markRaw(new THREE.MeshBasicMaterial({ color: 0xe53e3e }));
      const defendantMaterial = markRaw(new THREE.MeshBasicMaterial({ color: 0x38a169 }));
      const audienceMaterial = markRaw(new THREE.MeshBasicMaterial({ color: 0x4a5568 }));
      
      // 创建地面
      const floor = markRaw(new THREE.Mesh(
        markRaw(new THREE.PlaneGeometry(40, 60)), 
        floorMaterial
      ));
      floor.rotation.x = -Math.PI / 2;
      scene.add(floor);
      
      // 创建法官席
      const judgeDesk = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(10, 1, 3)), 
        judgeMaterial
      ));
      judgeDesk.position.set(0, 0.5, -20);
      scene.add(judgeDesk);
      
      // 创建法官椅
      const judgeChair = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(3, 1.5, 1.5)), 
        wallMaterial
      ));
      judgeChair.position.set(0, 0.75, -18);
      scene.add(judgeChair);
      
      // 创建原告席
      const plaintiffDesk = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(5, 0.8, 2)), 
        plaintiffMaterial
      ));
      plaintiffDesk.position.set(-7, 0.4, 0);
      scene.add(plaintiffDesk);
      
      const plaintiffChair = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(2, 1, 1)), 
        wallMaterial
      ));
      plaintiffChair.position.set(-7, 0.5, 1.5);
      scene.add(plaintiffChair);
      
      // 创建被告席
      const defendantDesk = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(5, 0.8, 2)), 
        defendantMaterial
      ));
      defendantDesk.position.set(7, 0.4, 0);
      scene.add(defendantDesk);
      
      const defendantChair = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(2, 1, 1)), 
        wallMaterial
      ));
      defendantChair.position.set(7, 0.5, 1.5);
      scene.add(defendantChair);
      
      // 创建观众席
      for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 8; col++) {
          const x = -8 + col * 2.5;
          const z = 5 + row * 2;
          
          const chair = markRaw(new THREE.Mesh(
            markRaw(new THREE.BoxGeometry(1, 0.8, 0.8)), 
            audienceMaterial
          ));
          chair.position.set(x, 0.4, z);
          scene.add(chair);
        }
      }
      
      // 添加标识
      addSimpleSign(0, 3, -20, judgeMaterial);
    };
    
    // 添加简单标识
    const addSimpleSign = (x, y, z, material) => {
      const sign = markRaw(new THREE.Mesh(
        markRaw(new THREE.BoxGeometry(2, 1, 0.1)), 
        material
      ));
      sign.position.set(x, y, z);
      scene.add(sign);
    };
    
    // 渲染场景
    const renderScene = () => {
      if (renderer && scene && camera) {
        renderer.render(scene, camera);
      }
    };
    
    // 动画循环
    const animateScene = () => {
      if (!isAnimating) return;
      
      // 旋转场景
      if (scene) {
        scene.rotation.y += rotationSpeed;
      }
      
      renderScene();
      animationId = requestAnimationFrame(animateScene);
    };
    
    // 窗口大小变化处理
    const onWindowResize = () => {
      if (!rendererContainer.value || !camera || !renderer) return;
      
      const width = rendererContainer.value.clientWidth;
      const height = rendererContainer.value.clientHeight;
      
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
      renderScene();
    };
    
    // 控制函数
    const rotateScene = () => {
      if (scene) {
        scene.rotation.y += 0.1;
        renderScene();
      }
    };
    
    const toggleAnimation = () => {
      isAnimating = !isAnimating;
      if (isAnimating) {
        animateScene();
      }
    };
    
    const zoomIn = () => {
      scaleLevel *= 1.1;
      if (camera) {
        camera.position.z /= 1.1;
        renderScene();
      }
    };
    
    const zoomOut = () => {
      scaleLevel *= 0.9;
      if (camera) {
        camera.position.z *= 1.1;
        renderScene();
      }
    };
    
    const viewFront = () => {
      if (camera && scene) {
        camera.position.set(0, 10, 30);
        camera.lookAt(0, 0, 0);
        scene.rotation.y = 0;
        renderScene();
      }
    };
    
    const viewTop = () => {
      if (camera && scene) {
        camera.position.set(0, 40, 0);
        camera.lookAt(0, 0, 0);
        scene.rotation.y = 0;
        renderScene();
      }
    };
    
    const viewSide = () => {
      if (camera && scene) {
        camera.position.set(30, 10, 0);
        camera.lookAt(0, 0, 0);
        scene.rotation.y = 0;
        renderScene();
      }
    };
    
    // 生命周期钩子
      onMounted(() => {
        // 已经在模板引用回调中初始化了
      });
    
    onBeforeUnmount(() => {
      window.removeEventListener('resize', onWindowResize);
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
      if (renderer) {
        if (renderer.domElement && renderer.domElement.parentNode) {
          renderer.domElement.parentNode.removeChild(renderer.domElement);
        }
        renderer.dispose();
      }
    });
    
    return {
        setRendererContainer,
        isAnimating,
        rotateScene,
        toggleAnimation,
        zoomIn,
        zoomOut,
        viewFront,
        viewTop,
        viewSide
      };
  }
};
</script>

<style scoped>
.court-3d-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: #1a1a2e;
}

.controls-panel {
  width: 300px;
  background-color: #16213e;
  padding: 20px;
  color: white;
  overflow-y: auto;
  border-right: 2px solid #0f3460;
}

.controls-panel h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #e94560;
  text-align: center;
}

.control-group {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #0f3460;
}

.control-group:last-child {
  border-bottom: none;
}

.control-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #64ffda;
}

.control-group button {
  margin: 5px;
  padding: 8px 12px;
  background-color: #0f3460;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-group button:hover {
  background-color: #e94560;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(233, 69, 96, 0.3);
}

.renderer-container {
  flex: 1;
  background-color: #1a1a2e;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .court-3d-container {
    flex-direction: column;
  }
  
  .controls-panel {
    width: 100%;
    height: auto;
    max-height: 300px;
  }
  
  .renderer-container {
    height: calc(100vh - 300px);
  }
}
</style>