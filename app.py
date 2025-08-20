import streamlit as st
import tempfile
import os
import sys

# Streamlit Community Cloud 환경설정
st.set_page_config(
    page_title="📄 Marker Document Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 디버그 정보
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 디버그 정보")
    if st.sidebar.button("🔍 환경 정보 표시"):
        st.sidebar.write(f"Python: {sys.version}")
        st.sidebar.write(f"Streamlit: {st.__version__}")
        try:
            import psutil
            memory = psutil.virtual_memory()
            st.sidebar.write(f"메모리: {memory.total//1024//1024//1024:.1f}GB 총량")
            st.sidebar.write(f"사용률: {memory.percent:.1f}%")
        except:
            st.sidebar.write("psutil 정보 없음")
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
    - 🚀 Hugging Face Spaces에서 16GB 메모리로 구동됩니다.
    - 📦 파일 크기 제한: 10MB 이하만 업로드 가능합니다.
    - 첫 실행 시 AI 모델 다운로드로 시간이 소요될 수 있습니다.
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
    
    # 파일 업로드 (크기 제한 추가)
    uploaded_file = st.file_uploader(
        "📁 문서 파일을 업로드하세요",
        type=['pdf', 'docx', 'pptx', 'xlsx', 'html', 'epub', 'png', 'jpg', 'jpeg'],
        help="지원 형식: PDF, DOCX, PPTX, XLSX, HTML, EPUB, PNG, JPG (최대 10MB)",
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        # 파일 정보 표시
        file_size = len(uploaded_file.getvalue())
        file_size_mb = file_size / 1024 / 1024
        
        # 파일 크기 제한 체크 (10MB)
        if file_size_mb > 10:
            st.error(f"❌ 파일 크기가 너무 큽니다: {file_size_mb:.1f}MB")
            st.error("🚫 Hugging Face Spaces는 10MB 이하의 파일만 지원합니다.")
            st.info("💡 더 작은 파일로 시도해주시거나, 로컬 환경에서 사용해주세요.")
            return
        
        st.success(f"✅ 파일 업로드 완료: {uploaded_file.name}")
        st.info(f"📊 파일 크기: {file_size:,} bytes ({file_size_mb:.1f} MB)")
        
        # 파일 타입 체크
        file_extension = uploaded_file.name.lower().split('.')[-1]
        if file_extension in ['pdf', 'docx', 'pptx', 'xlsx', 'html', 'epub', 'png', 'jpg', 'jpeg']:
            st.info(f"📄 파일 형식: {file_extension.upper()} (지원됨)")
        else:
            st.warning("⚠️ 지원되지 않는 파일 형식입니다.")
            return
        
        # 변환 버튼
        if st.button("🔄 변환 시작", type="primary"):
            try:
                st.info(f"🔄 변환 시작: {uploaded_file.name} ({file_size_mb:.1f}MB)")
                with st.spinner(f"🔄 {file_extension.upper()} 문서를 변환하는 중입니다... 잠시만 기다려주세요."):
                    # 임시 파일로 저장 (확장자에 맞게)
                    file_suffix = f'.{file_extension}'
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        # 메모리 사용량 체크 (Hugging Face Spaces 16GB)
                        try:
                            import psutil
                            memory_usage = psutil.virtual_memory()
                            st.info(f"📊 현재 메모리 사용률: {memory_usage.percent:.1f}% (사용가능: {memory_usage.available//1024//1024//1024:.1f}GB)")
                        except:
                            st.info("📊 Hugging Face Spaces 16GB 환경에서 실행 중")
                        
                        # Marker 패키지 import
                        from marker.converters.pdf import PdfConverter
                        from marker.converters.extraction import ExtractionConverter
                        from marker.models import create_model_dict
                        from marker.output import text_from_rendered
                        
                        st.success("✅ Marker 패키지 로드 완료!")
                        
                        # 진행 상태 표시
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("🔄 AI 모델 로딩 중...")
                        progress_bar.progress(10)
                        
                        # 파일 확장자는 이미 위에서 확인했음
                        st.info(f"🔍 처리할 파일: {uploaded_file.name} ({file_extension.upper()})")
                        
                        # AI 모델 로드 (Hugging Face Spaces 16GB 환경)
                        try:
                            model_dict = create_model_dict()
                            st.success("✅ AI 모델 로딩 완료!")
                        except Exception as model_error:
                            st.error("❌ AI 모델 로딩 실패")
                            st.error(f"상세 오류: {str(model_error)}")
                            st.info("💡 첫 실행 시 모델 다운로드에 시간이 걸릴 수 있습니다. 잠시 후 다시 시도해주세요.")
                            return
                        
                        progress_bar.progress(30)
                        
                        status_text.text(f"🔄 {file_extension.upper()} 문서 분석 중...")
                        
                        # 문서 변환 설정
                        config = {
                            "extract_images": extract_images,
                        }
                        
                        # 파일 타입에 따른 변환기 선택
                        if file_extension == 'pdf':
                            converter = PdfConverter(
                                artifact_dict=model_dict,
                                config=config
                            )
                        else:
                            # 다른 문서 형식은 ExtractionConverter 사용
                            converter = ExtractionConverter(
                                artifact_dict=model_dict,
                                config=config
                            )
                        progress_bar.progress(50)
                        
                        status_text.text("🔄 변환 실행 중...")
                        
                        # 변환 수행
                        rendered = converter(tmp_path)
                        progress_bar.progress(80)
                        
                        # 결과 추출
                        if output_format == "markdown":
                            result = text_from_rendered(rendered)
                        else:
                            result = str(rendered)  # JSON/HTML 형식
                        
                        progress_bar.progress(100)
                        status_text.text("✅ 변환 완료!")
                        
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
                    
                    except Exception as e:
                        error_msg = str(e)
                        st.error(f"❌ 변환 중 오류가 발생했습니다: {error_msg}")
                        
                        # 구체적인 에러 타입별 안내
                        if "403" in error_msg or "Forbidden" in error_msg:
                            st.error("🚫 403 Forbidden 오류 - Hugging Face Spaces 제한")
                            st.info("💡 이 오류는 HF Spaces의 네트워크 정책 또는 모델 다운로드 제한 때문일 수 있습니다.")
                            st.info("🔄 잠시 후 다시 시도하거나, 로컬 환경에서 사용해보세요.")
                        elif "Memory" in error_msg or "CUDA" in error_msg:
                            st.info("💡 메모리 부족 - 더 작은 파일로 시도해보세요.")
                        elif "timeout" in error_msg.lower():
                            st.info("💡 처리 시간 초과 - 더 단순한 문서로 시도해보세요.")
                        else:
                            st.info("💡 일시적 오류일 수 있습니다. 다시 시도해보세요.")
                    
                    finally:
                        # 임시 파일 정리
                        try:
                            os.unlink(tmp_path)
                        except:
                            pass
            
            except Exception as e:
                st.error(f"❌ 처리 중 오류가 발생했습니다: {str(e)}")
    
    # 연결 테스트
    with st.expander("🔧 연결 테스트"):
        if st.button("🌐 인터넷 연결 테스트"):
            try:
                import requests
                response = requests.get("https://httpbin.org/get", timeout=10)
                if response.status_code == 200:
                    st.success("✅ 인터넷 연결 정상")
                else:
                    st.error(f"❌ 연결 오류: {response.status_code}")
            except Exception as e:
                st.error(f"❌ 연결 실패: {str(e)}")
        
        if st.button("📦 Marker 패키지 테스트"):
            try:
                from marker.models import create_model_dict
                st.success("✅ Marker 패키지 import 성공")
                st.info("🔄 모델 딕셔너리 생성 테스트...")
                model_dict = create_model_dict()
                st.success("✅ AI 모델 로딩 성공!")
            except Exception as e:
                st.error(f"❌ Marker 테스트 실패: {str(e)}")
    
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