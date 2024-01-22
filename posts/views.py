from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer

import requests
from bs4 import BeautifulSoup

@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save()
            request.user.distribute_post_to_followers(post.id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_site_info(request):
    url = request.GET.get('url')

    if not url:
        return Response({'error': 'Missing "url" parameter'}, status=400)

    try:
        # Fetch HTML content from the URL using requests
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        html = response.text

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract relevant information
        title = soup.find('meta', {'property': 'og:title'})
        title = title['content'].strip() if title else ''
        #title = soup.title.text.strip() if soup.title else ''
        description = soup.find('meta', {'property': 'og:description'})
        description = description['content'].strip() if description else ''
        favicon = soup.find('link', {'rel': 'icon'})
        favicon = favicon['href'].strip() if favicon else ''
        site_name = soup.find('meta', {'property': 'og:site_name'})
        site_name = site_name['content'].strip() if site_name else ''

        # Find the image URL from the Open Graph Protocol meta tag
        og_image = soup.find('meta', {'property': 'og:image'})
        image_url = og_image['content'].strip() if og_image else ''

        # Return the extracted information using Django Rest Framework Response
        result = {
            'title': title,
            'description': description,
            'favicon': favicon,
            'sitename': site_name,
            'image': image_url,
        }

        return Response(result)

    except requests.RequestException as e:
        return Response({'error': f'Error fetching website information: {str(e)}'}, status=500)