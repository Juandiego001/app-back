from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.delivery import DeliveryIn, DeliveryOut, Deliveries
from app.services import delivery
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('delivery', __name__)


@bp.post('/')
@bp.input(DeliveryIn, location='form_and_files')
@bp.output(Message)
@jwt_required()
def create_delivery(form_and_files_data):
    '''
    Create delivery for activities
    :param data:
    '''
    try:
        form_and_files_data['userid'] = get_jwt()['_id']
        form_and_files_data['updated_by'] = get_jwt()['username']
        delivery.create_delivery(form_and_files_data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Deliveries)
def get_deliveries():
    '''
    Get deliveries
    '''
    try:
        return Deliveries().dump({'items': delivery.get_deliveries()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:deliveryid>')
@bp.output(DeliveryOut)
def get_delivery_detail(deliveryid):
    '''
    Get delivery detail
    '''
    try:
        return DeliveryOut().dump(
            delivery.get_delivery_by_id(deliveryid))
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:deliveryid>')
@bp.input(DeliveryIn)
@bp.output(Message)
def update_delivery(deliveryid, data):
    '''
    Update delivery
    :param data:
    '''
    try:
        delivery.update_delivery(deliveryid, data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.delete('/<string:deliveryid>')
@bp.output(Message)
@jwt_required()
def delete_delivery(deliveryid):
    '''
    Delete delivery
    '''
    try:
        delivery.delete_delivery(deliveryid)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))
