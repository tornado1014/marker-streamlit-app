import streamlit as st
import tempfile
import os
import sys

# Hugging Face Spaces 환경 설정 - 캐시 디렉토리 권한 문제 해결
os.environ['HF_HOME'] = '/tmp/huggingface'
os.environ['TRANSFORMERS_CACHE'] = '/tmp/huggingface/transformers'
os.environ['HF_DATASETS_CACHE'] = '/tmp/huggingface/datasets'
os.environ['MARKER_CACHE_DIR'] = '/tmp/marker_cache'
os.environ['XDG_CACHE_HOME'] = '/tmp/cache'
os.environ['TORCH_HOME'] = '/tmp/torch'
os.environ['HUGGINGFACE_HUB_CACHE'] = '/tmp/huggingface/hub'

# 캐시 디렉토리 생성
cache_dirs = [
    '/tmp/huggingface', '/tmp/marker_cache', '/tmp/cache', 
    '/tmp/huggingface/transformers', '/tmp/huggingface/datasets',
    '/tmp/torch', '/tmp/huggingface/hub'
]
for cache_dir in cache_dirs:
    os.makedirs(cache_dir, exist_ok=True)

# Streamlit Community Cloud 환경설정
st.set_page_config(
    page_title="📄 Marker Document Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📄 Marker Document to Markdown Converter")
    st.markdown("""
    이 앱은 **Marker**를 사용하여 다양한 문서를 마크다운으로 변환합니다.
    
    **지원 형식:**
    - 📄 **PDF** - Adobe PDF 문서
    - 📝 **DOCX** - Microsoft Word 문서  
    - 📊 **PPTX** - Microsoft PowerPoint 프레젠테이션
    - 📋 **XLSX** - Microsoft Excel 스프레드시트
    - 🌐 **HTML** - 웹 페이지 파일
    - 📚 **EPUB** - 전자책 파일
    - 🖼️ **Images** - PNG, JPG 이미지 파일
    
    **주의사항:**
    - Streamlit Community Cloud의 메모리 제한(1GB)으로 인해 대용량 파일 처리가 어려울 수 있습니다.
    - AI 모델 로딩에 대용량 메모리가 필요하여 클라우드에서 실행 제한이 있을 수 있습니다.
    - 복잡한 문서나 큰 파일은 로컬 환경에서 사용을 권장합니다.
    """)
    
    # 사이드바 설정
    st.sidebar.header("⚙️ 변환 설정")
    
    use_llm = st.sidebar.checkbox(
        "🤖 LLM 모드 사용",
        value=False,
        help="더 정확한 변환을 위해 LLM을 사용합니다 (느림)"
    )
    
    output_format = st.sidebar.selectbox(
        "📝 출력 형식",
        ["markdown", "json", "html"],
        index=0
    )
    
    extract_images = st.sidebar.checkbox(
        "🖼️ 이미지 추출",
        value=True,
        help="PDF에서 이미지를 추출합니다"
    )
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "📁 문서 파일을 업로드하세요",
        type=['pdf', 'docx', 'pptx', 'xlsx', 'html', 'epub', 'png', 'jpg', 'jpeg'],
        help="지원 형식: PDF, DOCX, PPTX, XLSX, HTML, EPUB, PNG, JPG (최대 200MB)"
    )
    
    if uploaded_file is not None:
        # 파일 정보 표시
        st.success(f"✅ 파일 업로드 완료: {uploaded_file.name}")
        st.info(f"📊 파일 크기: {len(uploaded_file.getvalue()):,} bytes")
        
        # 변환 버튼
        if st.button("🔄 변환 시작", type="primary"):
            try:
                with st.spinner("🔄 PDF를 변환하는 중입니다... 잠시만 기다려주세요."):
                    # 임시 파일을 /tmp 디렉토리에 생성 (권한 문제 해결)
                    file_extension = uploaded_file.name.lower().split('.')[-1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}', dir='/tmp') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        # 메모리 사용량 체크
                        import psutil
                        memory_usage = psutil.virtual_memory()
                        st.info(f"📊 현재 메모리 사용률: {memory_usage.percent:.1f}% (사용가능: {memory_usage.available/1024/1024/1024:.1f}GB)")
                        
                        # 캐시 디렉토리 확인 메시지
                        st.info(f"📁 캐시 디렉토리: {os.environ.get('MARKER_CACHE_DIR', '/tmp/marker_cache')}")
                        
                        if memory_usage.percent > 85:
                            st.warning("⚠️ 메모리 사용률이 높습니다. 변환이 실패할 수 있습니다.")
                        
                        # HF_TOKEN 환경변수 확인
                        hf_token = os.environ.get("HF_TOKEN")
                        if not hf_token:
                            st.warning("⚠️ HF_TOKEN 환경변수가 설정되지 않았습니다.")
                            st.info("💡 토큰 없이 모델 로딩을 시도합니다...")
                        
                        # Marker 패키지 import
                        from marker.convert import convert_single_pdf
                        from marker.models import load_all_models
                        
                        st.success("✅ Marker 패키지 로드 완료!")
                        
                        st.info("🔄 PDF 문서 분석 중...")
                        st.info(f"🔍 처리할 파일: {uploaded_file.name} ({uploaded_file.type.upper()})")
                        
                        # AI 모델 로딩 with progress spinner
                        with st.spinner("💡 AI 모델 로딩 중..."):
                            # 모델 로드 시 캐시 경로 명시적 지정
                            model_lst = load_all_models()
                            st.success("✅ AI 모델 로딩 완료!")
                        
                        # 변환 실행
                        with st.spinner("🔄 문서 변환 중..."):
                            full_text, images, out_meta = convert_single_pdf(
                                tmp_path,
                                model_lst,
                                extract_images=extract_images,
                                ocr_all_pages=use_llm
                            )
                        
                        # 출력 형식에 따른 결과 생성
                        if output_format == "markdown":
                            result = full_text
                        elif output_format == "json":
                            import json
                            result_data = {
                                "text": full_text,
                                "metadata": out_meta,
                                "images": len(images) if images else 0
                            }
                            result = json.dumps(result_data, ensure_ascii=False, indent=2)
                        else:  # html
                            result = f"<html><body><pre>{full_text}</pre></body></html>"
                        
                        # 결과 표시
                        st.success("🎉 변환이 완료되었습니다!")
                        
                        # 결과 다운로드
                        file_extension = "md" if output_format == "markdown" else output_format
                        st.download_button(
                            label=f"💾 {output_format.upper()} 파일 다운로드",
                            data=result,
                            file_name=f"converted.{file_extension}",
                            mime="text/plain"
                        )
                        
                        # 결과 미리보기 (일부만)
                        st.subheader("📄 변환 결과 미리보기")
                        
                        if output_format == "markdown":
                            # 마크다운 결과 표시 (처음 2000자)
                            preview = result[:2000] + ("..." if len(result) > 2000 else "")
                            st.markdown("```markdown\n" + preview + "\n```")
                        else:
                            # JSON/HTML 결과 표시
                            preview = result[:1000] + ("..." if len(result) > 1000 else "")
                            st.code(preview, language=output_format)
                    
                    except ImportError as e:
                        st.error("❌ Marker 패키지를 찾을 수 없습니다.")
                        st.error(f"오류 상세: {str(e)}")
                        st.info("💡 로컬에서만 사용 가능한 기능입니다.")
                    
                    except PermissionError as e:
                        if "/usr/local" in str(e) or "Permission denied" in str(e):
                            st.error("❌ 변환 중 오류가 발생했습니다: 시스템 파일 접근 권한 문제")
                            st.error(f"상세 오류: {str(e)}")
                            st.info("💡 일시적 오류일 수 있습니다. 다시 시도해보세요.")
                        else:
                            st.error(f"❌ 권한 오류: {str(e)}")
                    
                    except Exception as e:
                        st.error(f"❌ 변환 중 오류가 발생했습니다: {str(e)}")
                        st.info("💡 일시적 오류일 수 있습니다. 다시 시도해보세요.")
                    
                    finally:
                        # 임시 파일 정리
                        try:
                            os.unlink(tmp_path)
                        except:
                            pass
            
            except Exception as e:
                st.error(f"❌ 처리 중 오류가 발생했습니다: {str(e)}")
    
    # 사용법 가이드
    with st.expander("📖 사용법 가이드"):
        st.markdown("""
        ### 🚀 사용 방법
        1. **PDF 파일 업로드**: 변환할 PDF 파일을 선택합니다
        2. **설정 조정**: 왼쪽 사이드바에서 변환 옵션을 설정합니다
        3. **변환 실행**: "변환 시작" 버튼을 클릭합니다
        4. **결과 다운로드**: 변환이 완료되면 결과 파일을 다운로드합니다
        
        ### ⚙️ 설정 옵션
        - **LLM 모드**: 더 정확한 변환을 위해 AI를 추가로 사용 (느림)
        - **출력 형식**: Markdown, JSON, HTML 중 선택
        - **이미지 추출**: PDF의 이미지를 함께 추출
        
        ### ⚠️ 주의사항
        - 대용량 파일은 처리 시간이 오래 걸릴 수 있습니다
        - 복잡한 레이아웃의 PDF는 변환 결과가 완벽하지 않을 수 있습니다
        - Streamlit Community Cloud의 리소스 제한이 있습니다
        """)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            🔧 Powered by <a href='https://github.com/VikParuchuri/marker' target='_blank'>Marker</a> 
            | 📱 Built with <a href='https://streamlit.io' target='_blank'>Streamlit</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()