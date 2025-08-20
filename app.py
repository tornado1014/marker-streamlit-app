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
                    # 임시 파일로 저장
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        # 메모리 사용량 체크
                        import psutil
                        memory_usage = psutil.virtual_memory()
                        st.info(f"📊 현재 메모리 사용률: {memory_usage.percent:.1f}%")
                        
                        if memory_usage.percent > 85:
                            st.warning("⚠️ 메모리 사용률이 높습니다. 변환이 실패할 수 있습니다.")
                        
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
                        
                        # 파일 확장자 확인
                        file_extension = uploaded_file.name.lower().split('.')[-1]
                        
                        # 모델 로드 전 메모리 체크
                        if memory_usage.percent > 70:
                            st.error("❌ 메모리 부족으로 변환을 진행할 수 없습니다.")
                            st.info("💡 Streamlit Community Cloud의 메모리 제한으로 인해 대용량 AI 모델 로딩이 어렵습니다.")
                            return
                        
                        # 모델 로드 (메모리 제한으로 인해 실패할 수 있음)
                        try:
                            model_dict = create_model_dict()
                        except Exception as model_error:
                            st.error("❌ AI 모델 로딩 실패 - 메모리 부족")
                            st.error(f"상세 오류: {str(model_error)}")
                            st.info("💡 로컬 환경에서 사용하거나, 더 작은 문서로 시도해주세요.")
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
                        st.error(f"❌ 변환 중 오류가 발생했습니다: {str(e)}")
                        st.info("💡 파일이 너무 크거나 복잡할 수 있습니다. 더 작은 파일로 시도해보세요.")
                    
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