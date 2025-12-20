from django.utils.deprecation import MiddlewareMixin
from core.models import SiteVisit, AnimalView
from animals.models import AnimalProfile


class VisitTrackingMiddleware(MiddlewareMixin):
    """Track site visits and animal profile views"""
    
    def process_request(self, request):
        # Skip tracking for admin and static/media files
        if request.path.startswith('/admin/') or \
           request.path.startswith('/static/') or \
           request.path.startswith('/media/'):
            return None
        
        # Track general site visit
        try:
            SiteVisit.objects.create(
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                path=request.path,
                referer=request.META.get('HTTP_REFERER', ''),
                session_id=request.session.session_key or '',
            )
        except Exception:
            pass  # Don't break the site if tracking fails
        
        # Track animal profile views
        if '/animals/' in request.path and request.path != '/animals/':
            try:
                # Extract slug from path
                slug = request.path.split('/animals/')[-1].strip('/')
                if slug:
                    animal = AnimalProfile.objects.filter(slug=slug, archived=False).first()
                    if animal:
                        AnimalView.objects.create(
                            animal=animal,
                            ip_address=self.get_client_ip(request),
                            user_agent=request.META.get('HTTP_USER_AGENT', ''),
                            session_id=request.session.session_key or '',
                        )
                        # Update view count
                        animal.view_count += 1
                        animal.save(update_fields=['view_count'])
            except Exception:
                pass  # Don't break the site if tracking fails
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

