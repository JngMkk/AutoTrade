{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Colaboratory에 오신 것을 환영합니다",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/JngMkk/stzone/blob/main/stzone.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LSrwGanZ4ZJz",
        "outputId": "4eecab6e-fa27-4dbf-c4a4-771fd81e9605"
      },
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Mounted at /content/drive\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6U23R3Sw4mR1"
      },
      "source": [
        "from selenium import webdriver\n",
        "from bs4 import BeautifulSoup as bs\n",
        "import time\n",
        "import pandas as pd\n",
        "\n",
        "def page():\n",
        "    global driver\n",
        "    driver = webdriver.Chrome(r'C:\\Users\\JngMK\\Desktop\\2021KNUpython2/chromedriver')\n",
        "    url = 'https://strikes.zone/game/211115DSBKTW'\n",
        "    driver.get(url)\n",
        "    time.sleep(20)\n",
        "\n",
        "# 이닝별 버튼 클릭\n",
        "def inning_click():\n",
        "    driver.find_element_by_css_selector('div.match__type > button.type__btn.type__btn--inning').click()\n",
        "\n",
        "# 이닝별 판정, x좌표, y좌표 데이터 프레임(전역 변수)\n",
        "def inning():\n",
        "    innings = driver.find_elements_by_class_name('inning__view')\n",
        "    for inning in innings:\n",
        "        inning_index = innings.index(inning) + 1\n",
        "        stzone = inning.find_elements_by_class_name('strike__zone')[3]      # 4번째 그림 심판이 판정한 스트라이크 + 볼\n",
        "        svg = stzone.find_element_by_tag_name('svg')\n",
        "        imgs = svg.find_elements_by_tag_name('image')\n",
        "        xcd = []\n",
        "        ycd = []\n",
        "        sb = []\n",
        "        append1 = xcd.append\n",
        "        append2 = ycd.append\n",
        "        append3 = sb.append\n",
        "        for img in imgs:\n",
        "            append1(img.get_attribute('x'))\n",
        "            append2(img.get_attribute('y'))\n",
        "            if img.get_attribute('xlink:href') == '/_nuxt/img/1c8f58b.png' :\n",
        "                append3(1)\n",
        "            else :\n",
        "                append3(0)\n",
        "        globals()['cd_{}'.format(inning_index)] = pd.DataFrame({'이닝': [num * 0 + inning_index for num in sb],\n",
        "                                                                '판정': sb,\n",
        "                                                                'x좌표' : xcd, \n",
        "                                                                'y좌표' : ycd})\n",
        "       \n",
        "# 한 경기 모든 이닝 크롤링 + 엑셀 저장\n",
        "def inning_crawl():\n",
        "    games = driver.find_elements_by_class_name('search__data')\n",
        "    for game in games:\n",
        "        game.click()\n",
        "        time.sleep(10)\n",
        "        html = driver.page_source\n",
        "        time.sleep(3)\n",
        "        soup = bs(html, 'html.parser')\n",
        "        time.sleep(3)\n",
        "        match = soup.select('div.match__team > span')[0].text + ' ' + soup.select('div.match__team > span')[1].text + ' ' + soup.select('div.match__team > span')[2].text\n",
        "        date = soup.select_one('div.match__date').text.strip().split('투')[0]\n",
        "        referee = soup.select_one('div.match__date > span').text.split('(')[1].split('심')[0].split(' ')[0]\n",
        "        try :\n",
        "            inning()\n",
        "        except IndexError :\n",
        "            pass\n",
        "        inningcount = driver.find_elements_by_class_name('inning__view')\n",
        "        time.sleep(3)\n",
        "        if len(inningcount) == 15:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12,cd_13,cd_14,cd_15], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        elif len(inningcount) == 14:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12,cd_13,cd_14], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        elif len(inningcount) == 13:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12,cd_13], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        elif len(inningcount) == 12:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        elif len(inningcount) == 11:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        elif len(inningcount) == 10:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        elif len(inningcount) == 9:\n",
        "            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9], ignore_index = True)\n",
        "            df.index.names = [f'{date}_{match}_{referee}']\n",
        "            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')\n",
        "        else :\n",
        "            pass\n",
        "\n",
        "# 달력 넘기기\n",
        "def first_cal(num):\n",
        "    driver.find_element_by_class_name('strike__zone__wrapper').click()\n",
        "    driver.find_element_by_class_name('mx-input-wrapper').click()\n",
        "    time.sleep(2)\n",
        "    for i in range(num):\n",
        "        driver.find_element_by_class_name('mx-icon-last-month').click()\n",
        "        time.sleep(2)\n",
        "        if i == int(num) :\n",
        "            break\n",
        "\n",
        "# 날짜 넘어갈 때마다 달력 넘기기\n",
        "def last_cal(num):\n",
        "    driver.find_element_by_class_name('mx-input-wrapper').click()\n",
        "    time.sleep(2)\n",
        "    for i in range(num):\n",
        "        driver.find_element_by_class_name('mx-icon-last-month').click()\n",
        "        time.sleep(2)\n",
        "        if i == int(num) :\n",
        "            break\n",
        "\n",
        "# 크롤링\n",
        "def game_crawl(num):\n",
        "    for i in range(42):\n",
        "        month = driver.find_element_by_class_name('mx-panel.mx-panel-date')\n",
        "        day = month.find_elements_by_tag_name('td')[i]\n",
        "        time.sleep(2)\n",
        "        if day.get_attribute('class') == 'cell cur-month' :\n",
        "            day.click()\n",
        "            time.sleep(2)\n",
        "            driver.find_element_by_class_name('mx-datepicker-btn.mx-datepicker-btn-confirm').click()\n",
        "            time.sleep(10)\n",
        "            inning_crawl()\n",
        "            last_cal(num)\n",
        "        else :\n",
        "            continue\n",
        "\n",
        "# 최종\n",
        "def crawl(num):\n",
        "    first_cal(num)\n",
        "    game_crawl(num)\n",
        "\n",
        "# 2021.11 : 0 ~ 2021.04 : 7\n",
        "# 2020.11 : 12 ~ 2020.05 : 18\n",
        "# 2019.10 : 25 ~ 2019.03 : 32\n",
        "# 2018.11 : 36 ~ 2018.03 : 44\n",
        "# 2017.10 : 49 ~ 2017.03 : 56\n",
        "\n",
        "page()\n",
        "inning_click()\n",
        "crawl_months = [0,1,2,3,4,5,6,7,12,13,14,15,16,17,18,25,26,27,28,29,30,31,32,36,37,38,39,40,41,42,43,44,49,50,51,52,53,54,55,56]\n",
        "for i in crawl_months:\n",
        "    crawl(i)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "5fCEDCU_qrC0"
      },
      "source": [
        "<p><img alt=\"Colaboratory logo\" height=\"45px\" src=\"/img/colab_favicon.ico\" align=\"left\" hspace=\"10px\" vspace=\"0px\"></p>\n",
        "\n",
        "<h1>Colaboratory란?</h1>\n",
        "\n",
        "줄여서 'Colab'이라고도 하는 Colaboratory를 사용하면 브라우저에서 Python을 작성하고 실행할 수 있습니다. Colab은 다음과 같은 이점을 자랑합니다.\n",
        "- 구성이 필요하지 않음\n",
        "- GPU 무료 액세스\n",
        "- 간편한 공유\n",
        "\n",
        "<strong>학생</strong>이든, <strong>데이터 과학자</strong>든, <strong>AI 연구원</strong>이든 Colab으로 업무를 더욱 간편하게 처리할 수 있습니다. <a href=\"https://www.youtube.com/watch?v=inN8seMm7UI\">Colab 소개 영상</a>에서 자세한 내용을 확인하거나 아래에서 시작해 보세요."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "GJBs_flRovLc"
      },
      "source": [
        "## <strong>시작하기</strong>\n",
        "\n",
        "지금 읽고 계신 문서는 정적 웹페이지가 아니라 코드를 작성하고 실행할 수 있는 대화형 환경인 <strong>Colab 메모장</strong>입니다.\n",
        "\n",
        "예를 들어 다음은 값을 계산하여 변수로 저장하고 결과를 출력하는 간단한 Python 스크립트가 포함된 <strong>코드 셀</strong>입니다."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "id": "gJr_9dXGpJ05",
        "outputId": "9f556d03-ec67-4950-a485-cfdba9ddd14d"
      },
      "source": [
        "seconds_in_a_day = 24 * 60 * 60\n",
        "seconds_in_a_day"
      ],
      "execution_count": null,
      "outputs": [
        {
          "data": {
            "text/plain": [
              "86400"
            ]
          },
          "execution_count": 0,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2fhs6GZ4qFMx"
      },
      "source": [
        "위 셀의 코드를 실행하려면 셀을 클릭하여 선택한 후 코드 왼쪽의 실행 버튼을 누르거나 단축키 'Command/Ctrl+Enter'를 사용하세요. 셀을 클릭하면 코드 수정을 바로 시작할 수 있습니다.\n",
        "\n",
        "특정 셀에서 정의한 변수를 나중에 다른 셀에서 사용할 수 있습니다."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "id": "-gE-Ez1qtyIA",
        "outputId": "94cb2224-0edf-457b-90b5-0ac3488d8a97"
      },
      "source": [
        "seconds_in_a_week = 7 * seconds_in_a_day\n",
        "seconds_in_a_week"
      ],
      "execution_count": null,
      "outputs": [
        {
          "data": {
            "text/plain": [
              "604800"
            ]
          },
          "execution_count": 0,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "lSrWNr3MuFUS"
      },
      "source": [
        "Colab 메모장을 사용하면 <strong>실행 코드</strong>와 <strong>서식 있는 텍스트</strong>를 <strong>이미지</strong>, <strong>HTML</strong>, <strong>LaTeX</strong> 등과 함께 하나의 문서로 통합할 수 있습니다. Colab 메모장을 만들면 Google Drive 계정에 저장됩니다. Colab 메모장을 간편하게 공유하여 동료나 친구들이 댓글을 달거나 수정하도록 할 수 있습니다. 자세히 알아보려면 <a href=\"/notebooks/basic_features_overview.ipynb\">Colab 개요</a>를 참조하세요. 새 Colab 메모장을 만들려면 위의 파일 메뉴를 사용하거나 다음 링크로 이동하세요. <a href=\"http://colab.research.google.com#create=true\">새 Colab 메모장 만들기</a>\n",
        "\n",
        "Colab 메모장은 Colab에서 호스팅하는 Jupyter 메모장입니다. Jupyter 프로젝트에 관해 자세히 알아보려면 <a href=\"https://www.jupyter.org\">jupyter.org</a>를 참조하세요."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "UdRyKR44dcNI"
      },
      "source": [
        "## 데이터 과학\n",
        "\n",
        "Colab을 통해 인기 있는 Python 라이브러리를 최대한 활용하여 데이터를 분석하고 시각화할 수 있습니다. 아래 코드 셀에서는 <strong>Numpy</strong>를 사용하여 임의의 데이터를 생성하고 <strong>매트플롯립</strong>으로 이를 시각화합니다. 셀을 클릭하면 코드 수정을 바로 시작할 수 있습니다."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 281
        },
        "id": "C4HZx7Gndbrh",
        "outputId": "46abc637-6abd-41b2-9bba-80a7ae992e06"
      },
      "source": [
        "import numpy as np\n",
        "from matplotlib import pyplot as plt\n",
        "\n",
        "ys = 200 + np.random.randn(100)\n",
        "x = [x for x in range(len(ys))]\n",
        "\n",
        "plt.plot(x, ys, '-')\n",
        "plt.fill_between(x, ys, 195, where=(ys > 195), facecolor='g', alpha=0.6)\n",
        "\n",
        "plt.title(\"Sample Visualization\")\n",
        "plt.show()"
      ],
      "execution_count": null,
      "outputs": [
        {
          "data": {
            "image/png": "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\n/wEY0siNlckV2gAAAABJRU5ErkJggg==\n",
            "text/plain": [
              "<Figure size 432x288 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          },
          "output_type": "display_data"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "4_kCnsPUqS6o"
      },
      "source": [
        "Google Drive 계정에서 스프레드시트를 비롯한 데이터를 Colab 메모장으로 가져오거나 GitHub 등의 여러 다른 소스에서 데이터를 가져올 수 있습니다. Colab을 데이터 과학에 활용하는 방법과 데이터 가져오기에 관해 자세히 알아보려면 <a href=\"#working-with-data\">데이터 사용하기</a> 아래 링크를 참조하세요."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "OwuxHmxllTwN"
      },
      "source": [
        "## 머신러닝\n",
        "\n",
        "Colab을 사용하면 <a href=\"https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/quickstart/beginner.ipynb\">코드 몇 줄</a>만으로 이미지 데이터세트를 가져오고, 이 데이터세트로 이미지 분류기를 학습시키며, 모델을 평가할 수 있습니다. Colab 메모장은 Google 클라우드 서버에서 코드를 실행하므로 사용 중인 컴퓨터의 성능과 관계없이 <a href=\"#using-accelerated-hardware\">GPU 및 TPU</a>를 포함한 Google 하드웨어의 성능을 활용할 수 있습니다. 브라우저만 있으면 사용 가능합니다."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ufxBm1yRnruN"
      },
      "source": [
        "Colab은 다음과 같은 분야의 머신러닝 커뮤니티에서 널리 쓰이고 있습니다.\n",
        "- TensorFlow 시작하기\n",
        "- 신경망 개발 및 학습시키기\n",
        "- TPU로 실험하기\n",
        "- AI 연구 보급하기\n",
        "- 튜토리얼 만들기\n",
        "\n",
        "머신러닝 적용 사례를 보여 주는 Colab 메모장 샘플을 확인하려면 아래 <a href=\"#machine-learning-examples\">머신러닝 예시</a>를 참조하세요."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "-Rh3-Vt9Nev9"
      },
      "source": [
        "## 추가 리소스\n",
        "\n",
        "### Colab에서 메모장 사용하기\n",
        "- [Colaboratory 개요](/notebooks/basic_features_overview.ipynb)\n",
        "- [Markdown 가이드](/notebooks/markdown_guide.ipynb)\n",
        "- [라이브러리 가져오기 및 종속 항목 설치하기](/notebooks/snippets/importing_libraries.ipynb)\n",
        "- [GitHub에서 노트 저장 및 로드하기](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)\n",
        "- [대화형 양식](/notebooks/forms.ipynb)\n",
        "- [대화형 위젯](/notebooks/widgets.ipynb)\n",
        "- <img src=\"/img/new.png\" height=\"20px\" align=\"left\" hspace=\"4px\" alt=\"New\"></img>\n",
        " [Colab의 TensorFlow 2](/notebooks/tensorflow_version.ipynb)\n",
        "\n",
        "<a name=\"working-with-data\"></a>\n",
        "### 데이터로 작업하기\n",
        "- [데이터 로드: 드라이브, 스프레드시트, Google Cloud Storage](/notebooks/io.ipynb) \n",
        "- [차트: 데이터 시각화하기](/notebooks/charts.ipynb)\n",
        "- [BigQuery 시작하기](/notebooks/bigquery.ipynb)\n",
        "\n",
        "### 머신러닝 단기집중과정\n",
        "다음은 Google 온라인 머신러닝 과정에서 가져온 일부 메모장입니다. <a href=\"https://developers.google.com/machine-learning/crash-course/\">전체 과정 웹사이트</a>에서 자세한 내용을 확인하세요.\n",
        "- [Pandas DataFrame 소개](https://colab.research.google.com/github/google/eng-edu/blob/main/ml/cc/exercises/pandas_dataframe_ultraquick_tutorial.ipynb)\n",
        "- [합성 데이터를 사용하는 tf.keras 선형 회귀](https://colab.research.google.com/github/google/eng-edu/blob/main/ml/cc/exercises/linear_regression_with_synthetic_data.ipynb)\n",
        "\n",
        "\n",
        "<a name=\"using-accelerated-hardware\"></a>\n",
        "### 가속 하드웨어 사용하기\n",
        "- [GPU를 사용한 TensorFlow](/notebooks/gpu.ipynb)\n",
        "- [TPU를 사용한 TensorFlow](/notebooks/tpu.ipynb)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "P-H6Lw1vyNNd"
      },
      "source": [
        "<a name=\"machine-learning-examples\"></a>\n",
        "\n",
        "## 머신러닝 예시\n",
        "\n",
        "Colaboratory 덕분에 가능해진 대화형 머신러닝 분석의 예시를 자세히 살펴보려면 <a href=\"https://tfhub.dev\">TensorFlow Hub</a>의 모델을 사용한 이 튜토리얼을 살펴보세요.\n",
        "\n",
        "일부 추천 예시는 다음과 같습니다.\n",
        "\n",
        "- <a href=\"https://tensorflow.org/hub/tutorials/tf2_image_retraining\">이미지 분류기 재훈련</a>: 사전에 훈련된 이미지 분류기를 기반으로 꽃을 분류하기 위한 Keras 모델을 구축합니다.\n",
        "- <a href=\"https://tensorflow.org/hub/tutorials/tf2_text_classification\">텍스트 분류</a>: IMDB 영화 리뷰를 <em>긍정적인 리뷰</em> 또는 <em>부정적인 리뷰</em>로 분류합니다.\n",
        "- <a href=\"https://tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization\">스타일 트랜스퍼</a>: 딥 러닝을 사용하여 이미지 간에 스타일을 전이시킵니다.\n",
        "- <a href=\"https://tensorflow.org/hub/tutorials/retrieval_with_tf_hub_universal_encoder_qa\">Multilingual Universal Sentence Encoder Q&amp;A</a>: 머신러닝 모델을 사용하여 SQuAD 데이터 세트의 질문에 답변합니다.\n",
        "- <a href=\"https://tensorflow.org/hub/tutorials/tweening_conv3d\">동영상 보간 유형</a>: 동영상에서 첫 프레임과 마지막 프레임 사이에 발생한 내용을 예측합니다.\n"
      ]
    }
  ]
}